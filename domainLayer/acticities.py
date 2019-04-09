from flask import session,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    def register():
        print(request.form)
        userName=request.form['username']
        haveRegistered = db.session.query(security).filter_by(userName=request.form['username']).all()
        if haveRegistered.__len__() is not 0:
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
        return "register successful"
