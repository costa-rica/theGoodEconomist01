from folioApp import db


class Industrynames(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	series_id = db.Column(db.String(200), primary_key=True)
	industry_code = db.Column(db.String(100))
	product_code = db.Column(db.String(100))
	seasonal = db.Column(db.String(10))
	base_date = db.Column(db.String(10))
	series_title = db.Column(db.String(200))
	footnote_codes = db.Column(db.String(10))
	begin_year = db.Column(db.Integer)
	begin_period = db.Column(db.String(3))
	end_year = db.Column(db.Integer)
	end_period = db.Column(db.String(3))
	values = db.relationship('Industryvalues', backref='values', lazy=True)
    
    
	def __repr__(self):
		return f"Industrynames({self.series_id},{self.series_title})"

class Industryvalues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(200), db.ForeignKey('industrynames.series_id'))
    # series_id = db.Column(db.String(200), db.ForeignKey('industrynames.series_id'))
    year = db.Column(db.Integer)
    period = db.Column(db.String(3))
    value = db.Column(db.Float)
    footnote_codes = db.Column(db.String(10))
    # namesId = db.Column(db.Integer, db.ForeignKey('industrynames.id'))

    def __repr__(self):
        return f"Industryvalues({self.id},{self.series_id},{self.year},{self.period},{self.value})"


class Commoditynames(db.Model):
	series_id = db.Column(db.String(200), primary_key=True)
	group_code = db.Column(db.String(100))
	item_code = db.Column(db.String(100))
	seasonal = db.Column(db.String(10))
	base_date = db.Column(db.String(10))
	series_title = db.Column(db.String(200))
	footnote_codes = db.Column(db.String(10))
	begin_year = db.Column(db.Integer)
	begin_period = db.Column(db.String(3))
	end_year = db.Column(db.Integer)
	end_period = db.Column(db.String(3))
	values = db.relationship('Commodityvalues', backref='values', lazy=True)
    
    
	def __repr__(self):
		return f"Commoditynames({self.series_id},{self.series_title})"

class Commodityvalues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(200), db.ForeignKey('commoditynames.series_id'))
    year = db.Column(db.Integer)
    period = db.Column(db.String(3))
    value = db.Column(db.Float)
    footnote_codes = db.Column(db.String(10))


    def __repr__(self):
        return f"Commodityvalues({self.id},{self.series_id},{self.year},{self.period},{self.value})"