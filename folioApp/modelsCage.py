from folioApp import db

class Cagecompanies(db.Model):
    __bind_key__ = 'dbCage'
    CAGE_code = db.Column(db.String(5),primary_key=True)
    ADRS_NM_LN_NO__01 = db.Column(db.String(2))
    ADRS_NM_C_TXT1 = db.Column(db.String(36))
    ADRS_NM_LN_NO__2 = db.Column(db.String(2))
    ADRS_NM_C_TXT2 = db.Column(db.String(36))
    ST_ADDRESS1 = db.Column(db.String(36))
    ST_ADDRESS2 = db.Column(db.String(36))
    PO_BOX = db.Column(db.String(36))
    CITY = db.Column(db.String(36))
    ST_US_POSN = db.Column(db.String(2))
    ZIP_CODE = db.Column(db.String(10))
    COUNTRY = db.Column(db.String(36))
    TELEPHONE_NUMBER = db.Column(db.String(12))
    
    # def __init__(self, CAGE_code=None, ADRS_NM_LN_NO__01=None,ADRS_NM_C_TXT1=None,ADRS_NM_LN_NO__2=None,ADRS_NM_C_TXT2=None,ST_ADDRESS1=None,ST_ADDRESS2=None,PO_BOX=None,CITY=None,ST_US_POSN=None,ZIP_CODE=None,COUNTRY=None,TELEPHONE_NUMBER=None):
        # self.data =(CAGE_code,ADRS_NM_LN_NO__01,ADRS_NM_C_TXT1,ADRS_NM_LN_NO__2,ADRS_NM_C_TXT2,ST_ADDRESS1,ST_ADDRESS2,PO_BOX,CITY,ST_US_POSN,ZIP_CODE,COUNTRY,TELEPHONE_NUMBER)
    
    def __repr__(self):
        return f"Cagecompanies({self.CAGE_code},{self.ADRS_NM_C_TXT1},{self.ST_US_POSN})"
        # return f"Industrynames({self.series_id},{self.series_title})"