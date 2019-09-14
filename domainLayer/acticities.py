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
'''
This dictionary caches the copy trial Data. Key = participantID. 
Value = copyTrialID, copyTrialStartTime, staffID
'''
trialsData = {}

def routers(app):
    @app.route('/')
    def post():
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

    @app.route('/queryParticipantAll', methods=['POST'])
    def getParticipantInfo():
        print(request.form)
        keyword = request.form['keyword']
        result = []

        haveRecord = db.session.query(participants).filter(or_(participants.dateOfBirth.like('%'+str(keyword)+'%'),
                                                               participants.firstName.like('%'+str(keyword)+'%'),
                                                               participants.familyName.like('%'+str(keyword)+'%'),
                                                               participants.gender.like('%'+str(keyword)+'%'),
                                                               participants.participantID==str(keyword))).all()
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

        haveRecord = db.session.query(participants).filter(or_(participants.participantID==str(keyword))).all()
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
    def request_pixels2():  # First check the user id, then get pixel data of this user from database.
        print(request.headers)
        participant_id = request.form['username']
        target_trial = db.session.query(trials).filter_by(participantID=participant_id).all()
        recall_trialID= target_trial[0].recallTrialID
        copy_trialID= target_trial[0].copyTrialID

        target_copytrial = db.session.query(copy_trial).filter_by(copyTrialID=copy_trialID).all()
        target_recalltrial = db.session.query(recall_trial).filter_by(recallTrialID=recall_trialID).all()
        copy_trial_pixels = target_copytrial[0].copyTrialPixels
        recall_trial_pixels = target_recalltrial[0].recallTrialPixels
        print('copy pixels:'+copy_trial_pixels)
        print('recall pixels:' + recall_trial_pixels)
        print('Request for user pixel data, username:'+participant_id)
        if participant_id == 'sampleUser':
            return settings.samplePixelData+'&'+settings.samplePixelData2  # For testing
        else:
            # return settings.samplePixelData + '&' + settings.samplePixelData2  # For testing
            return copy_trial_pixels+'&'+recall_trial_pixels

    @app.route('/pixelsdata', methods=['GET'])
    def request_pixels():  # First check the user id, then get pixel data of this user from database.
        print(request.headers)
        participant_id = str(request.url).split("?")[1]
        print('participant_id:'+participant_id)
        target_trial = db.session.query(trials).filter_by(participantID=participant_id).all()
        if target_trial.__len__()!=0:
            recall_trialID= target_trial[0].recallTrialID
            copy_trialID= target_trial[0].copyTrialID

            target_copytrial = db.session.query(copy_trial).filter_by(copyTrialID=copy_trialID).all()
            target_recalltrial = db.session.query(recall_trial).filter_by(recallTrialID=recall_trialID).all()
            copy_trial_pixels = target_copytrial[0].copyTrialPixels
            recall_trial_pixels = target_recalltrial[0].recallTrialPixels
            print('copy pixels:'+copy_trial_pixels)
            print('recall pixels:' + recall_trial_pixels)
            print('Request for user pixel data, username:'+participant_id)
            if participant_id == 'sampleUser':
                return settings.samplePixelData+'&'+settings.samplePixelData2  # For testing
            else:
                # return settings.samplePixelData + '&' + settings.samplePixelData2  # For testing
                print(copy_trial_pixels+'&'+recall_trial_pixels)
                return copy_trial_pixels+'&'+recall_trial_pixels
        return "no record"

    '''
    The following 2 functions deal with uploading trial data to server.
    They receive data from client using POST method.
    '''
    @app.route('/uploadcopy', methods=['POST'])
    def upload_copy_trials():  # First check the user id, then get pixel data of this user from database.
        participant_id = request.form['username']  # The participant ID
        copy_trial_pixels = request.form['pixelData']
        time_data = request.form['timeData']
        staff_id = request.form['staffID']
        time_arr = time_data.split(';')
        copy_trial_start_time = time_arr[0]  # The time starting copy trial activity
        copy_trial_end_time = time_arr[3]  # The time clicking the finish button in copy trial activity
        print('Receive copy trial time data of user:' + participant_id + '\ndata:' + time_data)
        print('Receive copy trial pixel data of user:'+participant_id+'\ndata:'+copy_trial_pixels)
        create_copy_trial(participant_id, copy_trial_pixels, copy_trial_start_time, copy_trial_end_time, staff_id)
        return '1'  # Success

    @app.route('/uploadrecall', methods=['POST'])
    def upload_recall_pixels():
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
        create_recall_trial(participant_id, recall_trial_pixels, recall_trial_thinking_start_time,
                            recall_trial_thinking_end_time, recall_trial_drawing_start_time,
                            recall_trial_drawing_end_time)
        return '1'  # Success

    '''
    The following 3 functions deal with storing trials data to database
    
    '''
    def create_copy_trial(participant_id, copy_trial_pixels, copy_trial_start_time, copy_trial_end_time, staff_id):
        copy_trialInfo=copy_trial(copyTrialPixels=copy_trial_pixels,
                                  copyTrialStartTime=copy_trial_start_time,
                                  copyTrialEndTime=copy_trial_end_time)
        session.add(copy_trialInfo)
        session.flush()
        inserted_id = copy_trialInfo.copyTrialID
        session.commit()
        print("Copy Trial has been created with ID:"+str(inserted_id))
        temp_str = str(inserted_id)+','+str(copy_trial_start_time)+','+str(staff_id)
        trialsData[participant_id] = temp_str  # Cache data. Value = copyTrialID, copyTrialStartTime, staffID

    def create_recall_trial(participant_id, recall_trial_pixels, recall_trial_thinking_start_time,
                            recall_trial_thinking_end_time, recall_trial_drawing_start_time,
                            recall_trial_drawing_end_time):
        recall_trialInfo=recall_trial(recallTrialPixels=recall_trial_pixels,
                                      recallTrialThinkingStartTime=recall_trial_thinking_start_time,
                                      recallTrialThinkingEndTime=recall_trial_thinking_end_time,
                                      recallTrialDrawingStartTime=recall_trial_drawing_start_time,
                                      recallTrialDrawingEndTime=recall_trial_drawing_end_time)
        session.add(recall_trialInfo)
        session.flush()
        inserted_id = recall_trialInfo.recallTrialID
        session.commit()
        print("Recall Trial has been created with ID:"+str(inserted_id))
        tempArr = trialsData[participant_id].split(',')
        staff_id = tempArr[2]
        copy_trial_id = tempArr[0]
        trial_start_time = tempArr[1]
        create_trials(participant_id, staff_id, copy_trial_id, inserted_id, trial_start_time,
                      recall_trial_drawing_end_time)

    def create_trials(participant_id, staff_id, copy_trial_id, recall_trial_id, trial_start_time, trial_end_time):
        trialsInfo=trials(participantID=participant_id,
                          userName=staff_id,
                          copyTrialID=int(copy_trial_id),
                          recallTrialID=int(recall_trial_id),
                          trialStartTime=trial_start_time,
                          trialEndTime=trial_end_time)
        session.add(trialsInfo)
        session.flush()
        session.commit()
        print("Trial has been created")

