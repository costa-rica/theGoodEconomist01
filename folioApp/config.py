import os
import json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    with open(r'D:\OneDrive\Documents\professional\config_files\config_folioApp.json') as config_file:
        config = json.load(config_file)
elif os.environ.get('USER')=='sanjose':
    with open('/home/sanjose/Documents/environments/config.json') as config_file:
        config = json.load(config_file)
else:
    with open('/home/ubuntu/environments/config.json') as config_file:
        config = json.load(config_file)



class Config:
    SECRET_KEY = config.get('SECRET_KEY_DMR')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_BINDS ={'dbCage':config.get('SQLALCHEMY_BINDS_DBCAGE'),
        'dbSite' :config.get('SQLALCHEMY_BINDS_DBSITE')}
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_CBC')
    MAIL_USERNAME = config.get('MAIL_USERNAME_CBC')
    DEBUG = True
    STATIC_PATH =config.get('STATIC_PATH')
    GET_STS_FILES =config.get('GET_STS_FILES')
    PRICEINDICES=config.get('PRICEINDICES')
    REGISTRATION_KEY=config.get('REGISTRATION_KEY')
    BLS_API_URL=config.get('BLS_API_URL')

# class Config:
    # DEBUG = True
    # STATIC_PATH =r"folioApp/static"
    # GET_STS_FILES = r"folioApp/static/getSts"
    # PRICEINDICES = STATIC_PATH + '/priceindices'
    # SECRET_KEY = os.environ.get('SECRET_KEY_DMR')
    
    # SQLALCHEMY_DATABASE_URI = r"sqlite:///D:\databases\folioApp\folioApp.db"
    # SQLALCHEMY_BINDS = {'dbCage':r"sqlite:///D:\databases\folioApp\dbCage.db",
                        # 'dbSite' : r"sqlite:///D:\databases\folioApp\dbSite.db"}
    
    # REGISTRATION_KEY = 'dac9b184d4bd4208acc166c2c76ce129'
    # BLS_API_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'