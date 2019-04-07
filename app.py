
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
from flask import Flask
from flask import request
# from flask_script import Manager
import os
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import *
import settings
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+settings.username+":"+settings.password+"@"+settings.host+":3306/"+settings.databasename
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


engine=create_engine("mysql+pymysql://"+settings.username+":"+settings.password+"@"+settings.host+":3306/"+settings.databasename,echo=True)

metadata=MetaData(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

staff = Base.classes.staff
participants= Base.classes.participants
recall_trial=Base.classes.recall_trial
copy_trial=Base.classes.copy_trial
security=Base.classes.security
images=Base.classes.images
trails=Base.classes.trails

db=SQLAlchemy(app)
Session = sessionmaker(bind=engine)
session =Session()


@app.route('/', methods=['POST'])
def post():
    uid = request.form['uid']
    name =  request.form['name']
    print ('uid: %s, name: %s' % (uid, name))
    return 'OK.'

db.session.query(security).filter_by(userName="123").all()
@app.route('/stafflogin',methods=['POST'])
def check_user():
    userName=request.form['username']
    haveRegistered = db.session.query(security).filter_by(userName=request.form['username']).all()
    if haveRegistered.__len__() is not 0:
        passwordRight = db.session.query(security).filter_by(userName = request.form['username'],
                                              password = request.form['password']).all()
        if passwordRight.__len__() is not 0:
            print(str(userName) + "login successful")
            return "2" # 2 means login successful
        else:
            return "1" # 1 means password is not right
    else:
        print(str(userName) + "login fail")
        return "0" # 0 means not find username

@app.route('/registerstaff',methods=['POST'])
def register():
    print(request.form)
    userName=request.form['username']
    haveRegistered = db.session.query(security).filter_by(userName=request.form['username']).all()
    if haveRegistered.__len__() is not 0:
        return "0" # 0 means username has been registered
    staffInfo=staff(userName=request.form['username'],
                    firstName=request.form['firstname'],
                    familyName=request.form['familyname'],
                    dateOfBirth=request.form["dateofbirth"])
    securityInfo = security(userName=request.form['username'],password=request.form['password'])
    session.add(staffInfo)
    session.commit()
    session.add(securityInfo)
    session.commit()
    return "1" # 1 means register successful

if __name__ == '__main__':
    app.run()
