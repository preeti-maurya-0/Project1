from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#Instance of SQLAlchemy

db=SQLAlchemy() 

class Sponser(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sponser_company_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), unique=True,nullable=False)
    Industry = db.Column(db.Text,nullable=False)
    Budget=db.Column(db.Integer(),nullable=False)
    flagged_status=db.Column(db.Integer(),default=0)
    campaigns=db.relationship("Campaign",backref="sponsered",cascade="all,delete")
    
class Influencer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    influencer_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100),unique=True, nullable=False)
    niche = db.Column(db.Text,nullable=False)
    category = db.Column(db.Text,nullable=False)
    platform=db.Column(db.String(100), nullable=False)
    reach=db.Column(db.Integer(),nullable=False)
    flagged_status=db.Column(db.Integer(),default=0)
    Ads_request=db.relationship("Ad_request",backref="influencer",cascade="all,delete")
    # request=db.relationship("Request",backref=db.backref('sections',lazy=True))
   
class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    c_name = db.Column(db.String(100), nullable=False)
    visibility=db.Column(db.Integer(),default=0)
    description=db.Column(db.Text())
    budget=db.Column(db.Integer(),nullable=False)
    start_date=db.Column(db.Date, default=datetime.utcnow())
    end_date=db.Column(db.Date,nullable=False )
    campaign_status=db.Column(db.String(),default="pending")
    campaign_flagged_status=db.Column(db.Integer(),default=0)
    no_of_ads=db.Column(db.Integer(),default=0)
    progress=db.Column(db.Integer(),default=0)
    goal=db.Column(db.Text())
    sponser_id=db.Column(db.Integer(),db.ForeignKey("sponser.id"))
    niche=db.Column(db.Text())
    sponser_ads=db.relationship("Ad_request",backref="c_ads",cascade="all,delete")
   
class Ad_request(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    send_by=db.Column(db.Integer(),nullable=False)
    msg=db.Column(db.Text())
    requirements=db.Column(db.Text(),nullable=False)
    payment_amount=db.Column(db.Integer(),nullable=False)
    ad_request_status=db.Column(db.String(10),default="pending")
    nego=db.Column(db.Integer(),default=0)#nego=0 means does not want negotiation for this ad request , 1 for yes , want negotiation
    sponser_id=db.Column(db.Integer(),nullable=False)
    influencer_id=db.Column(db.Integer(),db.ForeignKey("influencer.id"))
    campaign_id=db.Column(db.Integer(),db.ForeignKey("campaign.id"),nullable=False)