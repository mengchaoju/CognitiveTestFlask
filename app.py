import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
from flask import Flask,current_app
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

db=SQLAlchemy(app)

# from datasourceLayer.databaseConnection import staff,security,recall_trial,copy_trial,trails,participants,images
from domainLayer.acticities import routers

routers(app)

if __name__ == '__main__':
    app.run()
