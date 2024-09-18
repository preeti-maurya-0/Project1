from flask_restful import Api,Resource,reqparse
from .models import *
api=Api()

 #parser for Ad_request
a_parser=reqparse.RequestParser()
a_parser.add_argument("msg")
a_parser.add_argument("requirements")
a_parser.add_argument("payment_amount")
a_parser.add_argument("influencer_id")
a_parser.add_argument("send_by")
a_parser.add_argument("ad_request_status")
a_parser.add_argument("nego")

#parser for sponser
s_parser=reqparse.RequestParser()
s_parser.add_argument("sponser_company_name")
s_parser.add_argument("password")
s_parser.add_argument("Industry")
s_parser.add_argument("Budget")
s_parser.add_argument("flagged_status")


#parser for influencer
i_parser=reqparse.RequestParser()
i_parser.add_argument("influencer_name")
i_parser.add_argument("password")
i_parser.add_argument("niche")
i_parser.add_argument("category")
i_parser.add_argument("flagged_status")
i_parser.add_argument("platform")
i_parser.add_argument("reach")



class AdRequestCampaignApi(Resource):

    def get(self,campaign_id):
        Ad_requests=Ad_request.query.filter_by(campaign_id=campaign_id).all()
        ad_requests=[]
        for ad in Ad_requests:
            ad_details={}
            ad_details['id']=ad.id
            ad_details['send_by']=ad.send_by
            ad_details['msg']=ad.msg
            ad_details['requirements']=ad.requirements
            ad_details['payment_amount']=ad.payment_amount
            ad_details['ad_request_status']=ad.ad_request_status
            ad_details['nego']=ad.nego
            ad_details['influencer_id']=ad.influencer_id
            ad_details['campaign_id']=ad.campaign_id
            ad_details['sponser_id_id']=ad.sponser_id_id
            ad_requests.append(ad_details)
        return ad_requests
    
    def post(self,campaign_id):
        ad_data=a_parser.parse_args()
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return "Campaign not found", 404

        if campaign.visibility==0:  # Assuming there's a boolean field 'is_public' in your Campaign model
            send_by = 0
        else:
            send_by = 1
        new_request=Ad_request(send_by=send_by,msg=ad_data["msg"],requirements=ad_data["requirements"],payment_amount=ad_data["payment_amount"],influencer_id=ad_data["influencer_id"],campaign_id=campaign_id,sponser_id=sponser_id)
        db.session.add(new_request)
        db.session.commit()
        return "Ad request created" ,201


class AdRequestApi(Resource):

    def put(self, ad_id):
        ad_data = a_parser.parse_args()
        ad = Ad_request.query.get(ad_id)
        if ad:
            ad.send_by = ad_data["send_by"]
            ad.msg = ad_data["msg"]
            ad.requirements = ad_data["requirements"]
            ad.payment_amount = ad_data["payment_amount"]
            ad.influencer_id = ad_data["influencer_id"]
            ad.ad_request_status=ad_data["ad_request_status"]
            ad.nego=ad_data["nego"]
            db.session.commit()
            return "Ad updated", 200
        else:
            return "Ad request not found", 404

    def delete(self, ad_id):
        ad = Ad_request.query.get(ad_id)
        if ad:
            db.session.delete(ad)
            db.session.commit()
            return "Ad request deleted", 200
        else:
            return "Ad request not found", 404



api.add_resource(AdRequestCampaignApi, "/api/adrequest/<int:campaign_id>")
api.add_resource(AdRequestApi, "/api/adrequest/<int:ad_id>")


class SponserApi(Resource):

    def get(self,sponser_id):
        sponser=Sponser.query.filter_by(id=sponser_id).first()
        spr={}
        spr["id"]=sponser.id
        spr["sponser_company_name"]=sponser.sponser_company_name
        spr["password"]=sponser.password
        spr["Industry"]=sponser.Industry
        spr["Budget"]=sponser.Budget
        spr["flagged_status"]=sponser.flagged_status
        return spr
    
    def post(self,sponser_id):
        s_data=s_parser.parse_args()
        new_user=Sponser(sponser_company_name=s_data["sponser_company_name"],password=s_data["password"],Industry=s_data["Industry"],Budget=s_data["Budget"],flagged_status=s_data["flagged_status"])
        db.session.add(new_user)
        db.session.commit()
        return "Sponser created" ,201
     
    def put(self, sponser_id):
        s_data=s_parser.parse_args()
        sr= Sponser.query.get(sponser_id)
        if sr:
            sr.sponser_company_name=s_data["sponser_company_name"]
            sr.password=s_data["password"]
            sr.Industry=s_data["Industry"]
            sr.Budget=s_data["Budget"]
            db.session.commit()
            return "Sponser updated", 200
        else:
            return "Sponser not found", 404

    def delete(self, sponser_id):
        sr = Sponser.query.get(sponser_id)
        if sr:
            db.session.delete(sr)
            db.session.commit()
            return "Sponser deleted", 200
        else:
            return "Sponser not found", 404

api.add_resource(SponserApi, "/api/sponser/<int:sponser_id>")





class InfluencerApi(Resource):

    def get(self,influencer_id):
        influencer=Influencer.query.filter_by(id=influencer_id).first()
        ir={}
        ir["id"]=influencer.id
        ir["influencer_name"]=influencer.influencer_name
        ir["password"]=influencer.password
        ir["niche"]=influencer.niche
        ir["category"]=influencer.category
        ir["reach"]=sponser.reach
        ir["platform"]=influencer.platform
        ir["flagged_status"]=sponser.flagged_status
        return ir
    
    def post(self,influencer_id):
        i_data=s_parser.parse_args()
        new_user=Influencer(influencer_name=i_data["influencer_name"],password=i_data["password"],niche=i_data["niche"],category=i_data["category"],flagged_status=i_data["flagged_status"],reach=i_data["reach"])
        db.session.add(new_user)
        db.session.commit()
        return "Influencer created" ,201
     
    def put(self, influencer_id):
        i_data=s_parser.parse_args()
        ir= Influencer.query.get(influencer_id)
        if ir:
            ir.influencer_name=i_data["influencer_name"]
            ir.password=i_data["password"]
            ir.niche=i_data["niche"]
            ir.category=i_data["category"]
            ir.reach=i_data["reach"]
            db.session.commit()
            return "influencer updated", 200
        else:
            return "influencer not found", 404

    def delete(self, influencer_id):
        ir = Influencer.query.get(sponser_id)
        if rr:
            db.session.delete(ir)
            db.session.commit()
            return "Influencer deleted", 200
        else:
            return "Influencer not found", 404

api.add_resource(InfluencerApi, "/api/influencer/<int:influencer_id>")