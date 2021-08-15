import os

class Config:
    DEBUG = True
    STATIC_PATH =r"folioApp/static"
    GET_STS_FILES = r"folioApp/static/getSts"
    PRICEINDICES = STATIC_PATH + '/priceindices'
    SECRET_KEY = os.environ.get('SECRET_KEY_DMR')
    
    SQLALCHEMY_DATABASE_URI = r"sqlite:///D:\databases\folioApp\folioApp.db"
    SQLALCHEMY_BINDS = {'dbCage':r"sqlite:///D:\databases\folioApp\dbCage.db",
                        'dbSite' : r"sqlite:///D:\databases\folioApp\dbSite.db"}
    
    REGISTRATION_KEY = 'dac9b184d4bd4208acc166c2c76ce129'
    BLS_API_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'