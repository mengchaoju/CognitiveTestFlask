from flask import session, request,Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json
import settings
from app import db
from datasourceLayer.databaseConnection import *
from sqlalchemy import or_,literal

engine = create_engine("mysql+pymysql://"+settings.username+":"+settings.password+"@"+settings.host+":3306/"+settings.databasename,echo=True)
Session = sessionmaker(bind=engine)
session = Session()
participant_id = 'sampleUser'  # The participant ID that requesting data
'''
The following global variables cache the data received from the app
'''
copy_trial_pixels = None
copy_trial_start_time = None
copy_trial_end_time = None
recall_trial_pixels = None
recall_trial_thinking_start_time = None
recall_trial_thinking_end_time = None
recall_trial_drawing_start_time = None
recall_trial_drawing_end_time = None


def routers(app):
    @app.route('/', methods=['POST'])
    def post():
        uid = request.form['uid']
        name = request.form['name']
        print('uid: %s, name: %s' % (uid, name))
        return 'OK.'

    @app.route('/stafflogin', methods=['POST'])
    def check_user():
        userName = request.form['username']
        haveRegistered = db.session.query(security).filter_by(userName=request.form['username']).all()
        if haveRegistered.__len__() is not 0:
            passwordRight = db.session.query(security).filter_by(userName = request.form['username'],
                                                  password = request.form['password']).all()
            if passwordRight.__len__() is not 0:
                print(str(userName) + "login successful")
                return "login successful"
            else:
                return "password is not right"
        else:
            print(str(userName) + " :login fail")
            return "not find username"

    @app.route('/registerstaff',methods=['POST'])
    def registerStaff():
        print(request.form)
        userName=request.form['username']
        haveRegistered = db.session.query(security).filter_by(userName=request.form['username']).all()
        if haveRegistered.__len__() is not 0:
            print("username has been registered")
            return "username has been registered"
        staffInfo=staff(userName=request.form['username'],
                        firstName=request.form['firstname'],
                        familyName=request.form['familyname'],
                        dateOfBirth=request.form["dateofbirth"])
        securityInfo = security(userName=request.form['username'], password=request.form['password'])
        session.add(staffInfo)
        session.commit()
        session.add(securityInfo)
        session.commit()
        print("register successful")
        return "register successful"

    @app.route('/registerParticipant', methods=['POST'])
    def registerParticipants():
        print(request.form)
        mParticipantID = request.form['participantid']
        mFirstName = request.form['firstname']
        mFamilyName = request.form['familyname']
        mParticipantID = request.form['participantid']
        mGender = request.form['gender']
        mDateOfBirth = request.form['dateofbirth']
        haveRegistered = db.session.query(participants).filter_by(participantID=request.form['participantid']).all()
        if haveRegistered.__len__() is not 0:
            return "participant ID has been registered"
        participantsInfo=participants(participantID=mParticipantID,
                                      firstName=mFirstName,
                                      familyName=mFamilyName,
                                      gender=mGender,
                                      dateOfBirth=mDateOfBirth)
        session.add(participantsInfo)
        session.commit()
        print("participant register successfully")
        return "participant register successfully"

    @app.route('/createImage',methods=['POST'])
    def createImage():
        print(request.form)
        imageInfo=images(imageName=request.form['imagename'],
                                  image=request.form['image']
                        )
        session.add(imageInfo)
        session.flush()
        session.commit()
        # inserted_id = recall_trialInfo.recallTrailID
        print("Recall Trial has been created")
        return "image has been created successfully"

    @app.route('/queryParticipantAll', methods=['POST'])
    def getParticipantInfo():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.dateOfBirth.like('%'+str(keyword)+'%'),
                                                               participants.firstName.like('%'+str(keyword)+'%'),
                                                               participants.familyName.like('%'+str(keyword)+'%'),
                                                               participants.gender.like('%'+str(keyword)+'%'),
                                                               participants.dateOfBirth.like('%' + str(keyword) + '%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/queryParticipantFirstName', methods=['POST'])
    def getParticipantFirst():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.firstName.like('%'+str(keyword)+'%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/queryParticipantFamilyName', methods=['POST'])
    def getParticipantFamily():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.familyName.like('%'+str(keyword)+'%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/queryParticipantID', methods=['POST'])
    def getParticipantID():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.participantID.like('%'+str(keyword)+'%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/queryParticipantGender', methods=['POST'])
    def getParticipantGender():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.gender.like('%'+str(keyword)+'%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/queryParticipantDateOfBirth', methods=['POST'])
    def getParticipantDoB():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.dateOfBirth.like('%'+str(keyword)+'%'))).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record={
                    "participantid":i.participantID,
                    "firstname": i.firstName,
                    "familyname":i.familyName,
                    "gender": i.gender,
                    "dateofbirth":i.dateOfBirth
                }

                result.append(record)

        if result.__len__()==0:
            print("no record on :"+ keyword)
            return "No record"
        else:
            resultJson=json.dumps(result)
            return resultJson

    @app.route('/pixelsdata', methods=['POST'])
    def request_pixels():  # First check the user id, then get pixel data of this user from database.
        global participant_id
        participant_id = request.form['username']
        print('Request for user pixel data, username:'+participant_id)
        if participant_id == 'sampleUser':
            return settings.samplePixelData+'&'+settings.samplePixelData2  # For testing
        else:
            return settings.samplePixelData+'&'+settings.samplePixelData2  # For testing


    '''
    The following 2 functions deal with uploading trial data to server.
    They receive data from client using POST method.
    '''
    @app.route('/uploadcopy', methods=['POST'])
    def upload_copy_trials():  # First check the user id, then get pixel data of this user from database.
        global participant_id, copy_trial_pixels
        global copy_trial_start_time, copy_trial_end_time
        participant_id = request.form['username']  # The participant ID
        copy_trial_pixels = request.form['pixelData']
        time_data = request.form['timeData']
        time_arr = time_data.split(';')
        copy_trial_start_time = time_arr[0]  # The time starting copy trial activity
        copy_trial_end_time = time_arr[3]  # The time clicking the finish button in copy trial activity
        print('Receive copy trial time data of user:' + participant_id + '\ndata:' + time_data)
        print('Receive copy trial pixel data of user:'+participant_id+'\ndata:'+copy_trial_pixels)
        create_copy_trail()
        return '1'  # Success
        haveRecord = db.session.query(participants).filter_by(gender=keyword).all()
        if haveRecord.__len__() is not 0:
            for i in haveRecord:
                record = {
                    "participantid": i.participantID,
                    "firstname": i.firstName,
                    "familyname": i.familyName,
                    "gender": i.gender,
                    "dateofbirth": i.dateOfBirth
                }
                result.append(record)

    @app.route('/uploadrecall', methods=['POST'])
    def upload_recall_pixels():
        global participant_id, recall_trial_pixels
        global recall_trial_thinking_start_time, recall_trial_thinking_end_time
        global recall_trial_drawing_start_time, recall_trial_drawing_end_time
        participant_id = request.form['username']
        recall_trial_pixels = request.form['pixelData']
        time_data = request.form['timeData']
        time_arr = time_data.split(';')
        recall_trial_thinking_start_time = time_arr[0]
        recall_trial_thinking_end_time = time_arr[1]
        recall_trial_drawing_start_time = time_arr[2]
        recall_trial_drawing_end_time = time_arr[3]
        print('Receive recall trial time data of user:' + participant_id + '\ndata:' + time_data)
        print('Receive recall trial pixel data of user:' + participant_id + '\ndata:' + recall_trial_pixels)
        create_recall_trail()
        return '1'  # Success

    '''
    The following 3 functions deal with storing trials data to database
    
    '''
    def create_copy_trail():
        global copy_trial_pixels, copy_trial_start_time, copy_trial_end_time
        copy_trialInfo=copy_trial(copyTrialPixels=copy_trial_pixels,
                                  copyTrialStartTime=copy_trial_start_time,
                                  copyTrialEndTime=copy_trial_end_time)
        session.add(copy_trialInfo)
        session.flush()
        inserted_id = copy_trialInfo.copyTrialID
        session.commit()
        print("Copy Trial has been created with ID:"+str(inserted_id))

    def create_recall_trail():
        global recall_trial_pixels, recall_trial_thinking_start_time, recall_trial_thinking_end_time
        global recall_trial_drawing_start_time, recall_trial_drawing_end_time
        recall_trialInfo=recall_trial(recallTrialPixels=recall_trial_pixels,
                                      recallTrailThinkingStartTime=recall_trial_thinking_start_time,
                                      recallTrailThinkingEndTime=recall_trial_thinking_end_time,
                                      recallTrailDrawingStartTime=recall_trial_drawing_start_time,
                                      recallTrailDrawingEndTime=recall_trial_drawing_end_time)
        session.add(recall_trialInfo)
        session.flush()
        inserted_id = recall_trialInfo.recallTrailID
        session.commit()
        # inserted_id = recall_trialInfo.recallTrailID
        print("Recall Trial has been created with ID:"+str(inserted_id))

    def createTrails():
        global participant_id
        trailsInfo=trails(participantID=participant_id,
                          userName=request.form['username'],
                          copyTrialID=request.form['copytrailid'],
                          recallTrailID=request.form['recalltrailid'],
                          trialStartTime=request.form['trialstarttime'],
                          trailEndTime=request.form['trailendtime']
                          )
        session.add(trailsInfo)
        session.flush()
        session.commit()
        print("Trail has been created")
        print("Trail has been created successful")

