from flask import session,request,Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json
import settings
from app import db
from datasourceLayer.databaseConnection import *

engine=create_engine("mysql+pymysql://"+settings.username+":"+settings.password+"@"+settings.host+":3306/"+settings.databasename,echo=True)
Session = sessionmaker(bind=engine)
session =Session()

def routers(app):
    @app.route('/', methods=['POST'])
    def post():
        uid = request.form['uid']
        name =  request.form['name']
        print ('uid: %s, name: %s' % (uid, name))
        return 'OK.'

    @app.route('/stafflogin',methods=['POST'])
    def check_user():
        userName=request.form['username']
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
            print(str(userName) + "login fail")
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
        securityInfo = security(userName=request.form['username'],password=request.form['password'])
        session.add(staffInfo)
        session.commit()
        session.add(securityInfo)
        session.commit()
        print("register successful")
        return "register successful"

    @app.route('/registerParticipant',methods=['POST'])
    def registerParticipants():
        print(request.form)
        participantsID = request.form['patricipantsID']
        haveRegistered = db.session.query(security).filter_by(participantsID=request.form['participantsid']).all()
        if haveRegistered.__len__() is not 0:
            return "participant ID has been registered"
        participantsInfo=participants(participantsID=request.form['participantsid'],
                                      firstName=request.form['firstName'],
                                      familyName=request.form['familyname'],
                                      gender=request.form['gender'],
                                      dob=request.form['dateofbirth'])
        session.add(participantsInfo)
        session.commit()
        print("participant register successfully")
        return "participant register successfully"

    @app.route('/createCopyTrial',methods=['POST'])
    def createCopyTrail():
        print(request.form)
        copy_trialInfo=copy_trial(copyTrialID=request.form['copytrialid'],
                                  copyTrialPixels=request.form['copytrialpixels'],
                                  copyTrialStartTime=request.form['copytrialstarttime'],
                                  copyTrialEndTime=request.form['copytrialendtime'])
        session.add(copy_trialInfo)
        session.flush()
        inserted_id=copy_trialInfo.copyTrialID
        session.commit()
        print("Copy Trial has been created")
        return str(inserted_id)

    @app.route('/createRecallTrial',methods=['POST'])
    def createRecallTrail():
        print(request.form)
        recall_trialInfo=recall_trial(recallTrialPixels=request.form['recalltrialpixels'],
                                  recallTrailThinkingStartTime=request.form['recalltrialthinkingstarttime'],
                                  recallTrailThinkingEndTime=request.form['recalltrialthinkingendtime'],
                                  recallTrailDrawingStartTime=request.form['recalltrialdrawingstarttime'],
                                  recallTrailDrawingEndTime=request.form['recalltrialdrawingendtime'])
        session.add(recall_trialInfo)
        session.flush()
        instered_id=recall_trialInfo.recallTrailID
        session.commit()
        # inserted_id = recall_trialInfo.recallTrailID
        print("Recall Trial has been created")
        return str(instered_id)

    @app.route('/createTrails',methods=['POST'])
    def createTrails():
        print(request.form)
        trailsInfo=trails(participantID=request.form['paeticipantid'],
                          userName = request.form['username'],
                          copyTrialID=request.form['copytrailid'],
                          recallTrailID=request.form['recalltrailid'],
                          trialStartTime=request.form['trialstarttime'],
                          trailEndTime=request.form['trailendtime']
                          )
        session.add(trailsInfo)
        session.flush()
        session.commit()
        print("Trail has been created")
        return "Trail has been created successful"

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

    @app.route('/queryParticipantByDoB', methods=['GET'])
    def getParticipantInfoByDoB():
        print(request.form)
        participantsDoB = request.form['dateofbirth']
        request.args.get()
        result = []
        haveRecord = db.session.query(participants).filter_by(dataOfBirth=request.form['dateofbirth']).all()
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
        else:
            print("no record on"+ participantsDoB)
            return "no record"




