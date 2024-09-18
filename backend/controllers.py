from flask import flash,render_template,redirect,request
from app import app  # Import the app instance created in app.py
from .models import *
from sqlalchemy import func
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend

import matplotlib.pyplot as plt







@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        username=request.form.get("admin_name")
        password=request.form.get("pwd")
        if username=="Preeti Maurya" and password=="1004":
            total_campaigns=Campaign.query.all()
            total_sponsers=Sponser.query.all()
            total_influencers=Influencer.query.all()
            active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
            active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
            flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
            active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
            flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
            active_influencers=Influencer.query.filter_by(flagged_status=0).all()
            flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
            total_ad_request=Ad_request.query.all() 
            Insc_summary()
            return render_template("admin_dashboard.html",total_sponsers=total_sponsers,total_influencer=total_influencers,name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,total_campaigns=total_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)

        else:
            return render_template("admin_login.html")
    return render_template("admin_login.html")


@app.route("/login", methods=["GET","POST"])
def user_login():
    if request.method=="POST":
        user_type=request.form.get("guser_type")
        username=request.form.get("guser_name")
        password=request.form.get("gpwd")
        if user_type=="0":
            usr=Sponser.query.filter_by(sponser_company_name=username,password=password).first()
            if usr and usr.flagged_status==0:
                return redirect(f'/sponser_dashboard/{usr.id}')
            else:
                return render_template("user_login.html",msg="Sponser does not exist!!")
        elif user_type=="1":
            usr=Influencer.query.filter_by(influencer_name=username,password=password).first()
            if usr and usr.flagged_status==0:
                return redirect(f'/influencer_dashboard/{usr.id}')
            else:
                return render_template("user_login.html",msg="Influencer does not exist!!")
    return render_template("user_login.html",msg="")


@app.route("/influencer_registration",methods=["GET","POST"])
def influencer_registration():
    if request.method=="POST":
        username=request.form.get("guser_name")
        password=request.form.get("gpwd")
        niche=request.form.get("niche")
        category=request.form.get("category")
        reach=request.form.get("reach")
        platform=request.form.get("platform")
        user=Influencer.query.filter_by(password=password).first()
        if not user:
            new_user=Influencer(influencer_name=username,password=password,niche=niche,category=category,reach=reach,platform=platform)
            db.session.add(new_user)
            db.session.commit()
            return render_template("user_login.html",msg="")
        else:
            return render_template("influencer_registration.html",msg="sorry! user already exist!!")
    return render_template("influencer_registration.html",msg="")


@app.route("/sponser_registration",methods=["GET","POST"])
def sponser_registration():
    if request.method=="POST":
        username=request.form.get("guser_name")
        password=request.form.get("gpwd")
        industry=request.form.get("industry")
        budget=int(request.form.get("budget"))
        user=Sponser.query.filter_by(password=password).first()
        if not user:
            new_user=Sponser(sponser_company_name=username,password=password,Industry=industry,Budget=budget)
            db.session.add(new_user)
            db.session.commit()
            return render_template("user_login.html",msg="")
        else:
            return render_template("sponser_registration.html",msg="sorry! user already exist!!")
    return render_template("sponser_registration.html",msg="")




@app.route("/admin_find",methods=["GET","POST"])
def admin_find():
    all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0).all()
    if request.method=="POST":
        criteria=request.form.get("criteria")
        search=request.form.get("search")
        search =search.strip().lower()
        if criteria=="campaigns":
            if search=="public":
               campaigns=Campaign.query.filter_by(visibility=0,campaign_flagged_status=0).all()
               return render_template("admin_find.html",campaigns=campaigns,msg="")
            elif search=="private":
                campaigns=Campaign.query.filter_by(visibility=1,campaign_flagged_status=0).all()
                return render_template("admin_find.html",campaigns=campaigns,msg="")
            elif search=="active":
                campaigns=Campaign.query.filter_by(campaign_status="accepted",campaign_flagged_status=0).all()
                return render_template("admin_find.html",campaigns=campaigns,msg="")
            elif search=="flagged":
                fcampaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
                return render_template("admin_find.html",fcampaigns=fcampaigns,msg="")
            elif search=="all":
                campaigns=Campaign.query.filter_by(campaign_flagged_status=0).all()
                return render_template("admin_find.html",campaigns=campaigns,msg="")
            elif search=="":
                campaigns=Campaign.query.filter_by(campaign_flagged_status=0).all()
                return render_template("admin_find.html",campaigns=campaigns,msg="")  
            else:
                msg="No such campaign available!! try something else"
                return render_template("admin_find.html",msg=msg)
            
        if criteria=="influencers":
            if search=="flagged":
               finfluencers=Influencer.query.filter_by(flagged_status=1).all()
               return render_template("admin_find.html",finfluencers=finfluencers,msg="")
            elif search=="active":
                influencers=Influencer.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",influencers=influencers,msg="")
            elif search in ['mostreach','most reach','most followers','mostfollowers','greater than 100000']:
                influencers = Influencer.query.filter(Influencer.reach > 100000).all()
                return render_template("admin_find.html",influencers=influencers,msg="")
            elif search=="all":
                influencers=Influencer.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",influencers=influencers,msg="")
            elif search=="":
                influencers=Influencer.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",influencers=influencers,msg="")
            else:
                msg="No such influencers available!! try something else"
                return render_template("admin_find.html",msg=msg) 
            

        if criteria=="sponsers":
            if search=="flagged":
               fsponsers=Sponser.query.filter_by(flagged_status=1).all()
               return render_template("admin_find.html",fsponsers=fsponsers,msg="")
            elif search=="active":
                sponsers=Sponser.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",sponsers=sponsers,msg="")
            elif search in ['mostbudget','greater budget','greater than 100000']:
                sponsers = Sponser.query.filter(Sponser.budget > 100000).all()
                return render_template("admin_find.html",sponsers=sponsers,msg="")
            elif search=="all":
                sponsers=Sponser.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",sponsers=sponsers,msg="")
            elif search=="":
                sponsers=Sponser.query.filter_by(flagged_status=0).all()
                return render_template("admin_find.html",sponsers=sponsers,msg="")
            else:
                msg="No such sponsers available!! try something else"
                return render_template("admin_find.html",msg=msg) 
            

        if criteria=="ad_requests":
            if search=="accepted":
               ad_requests=Ad_request.query.filter_by(ad_request_status="accepted").all()
               return render_template("admin_find.html",ad_requests=ad_requests,msg="")
            elif search=="rejected":
                ad_requests=Ad_request.query.filter_by(ad_request_status="rejected").all()
                return render_template("admin_find.html",ad_requests=ad_requests,msg="")
            elif search=="all":
                ad_requests=Ad_request.query.all()
                return render_template("admin_find.html",ad_requests=ad_requests,msg="")
            elif search=="":
                ad_requests=Ad_request.query.all()
                return render_template("admin_find.html",ad_requests=ad_requests,msg="")
            else:
                msg="No such ad request available!! try something else"
                return render_template("admin_find.html",msg=msg) 
            
    else:
        return render_template("admin_find.html",all_campaigns=all_campaigns)   


@app.route("/flag_campaign",methods=["GET","POST"])
def flag_campaign():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        c_id=request.form.get("campaign_id")
        campaign=Campaign.query.get(c_id)
        campaign.campaign_flagged_status=1
        ads=Ad_request.query.filter_by(campaign_id=c_id).all()
        for ad in ads:
            db.session.delete(ad)
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
     
   


@app.route("/flag_sponser",methods=["GET","POST"])
def flag_sponser():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        s_id=request.form.get("sponser_id")
        sponser=Sponser.query.get(s_id)
        sponser.flagged_status=1
        cs=Campaign.query.filter_by(sponser_id=s_id).all()
        for c in cs:
            c.campaign_flagged_status=1
            ads=Ad_request.query.filter_by(campaign_id=c.id).all()
            for ad in ads:
                db.session.delete(ad)
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    
@app.route("/flag_influencer",methods=["GET","POST"])
def flag_influencer():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        i_id=request.form.get("influencer_id")
        influencer=Influencer.query.get(i_id)
        influencer.flagged_status=1
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    

@app.route("/unflag_campaign",methods=["GET","POST"])
def unflag_campaign():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        c_id=request.form.get("campaign_id")
        campaign=Campaign.query.get(c_id)
        campaign.campaign_flagged_status=0
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    


@app.route("/unflag_sponser",methods=["GET","POST"])
def unflag_sponser():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        s_id=request.form.get("sponser_id")
        sponser=Sponser.query.get(s_id)
        sponser.flagged_status=0
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    
@app.route("/unflag_influencer",methods=["GET","POST"])
def unflag_influencer():
    username="Preeti Maurya"
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    total_ad_request=Ad_request.query.all() 
    if request.method=="POST":
        i_id=request.form.get("influencer_id")
        influencer=Influencer.query.get(i_id)
        influencer.flagged_status=0
        db.session.commit()
        return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    return render_template("admin_dashboard.html",name=username,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=total_ad_request)    
    



# sponser routings
            
    

@app.route("/sponser_dashboard/<int:sponser_id>")
def sponser_dashboard(sponser_id):
    sponser = Sponser.query.get_or_404(sponser_id)
    active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
    newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
    nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
    return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)
    

@app.route("/sponser_profile/<int:sponser_id>")
def sponser_profile(sponser_id):
    sponser = Sponser.query.get_or_404(sponser_id)
    return render_template("sponser_profile.html",i_user=sponser)


@app.route("/update_sponser_profile/<int:sponser_id>",methods=["GET","POST"])
def update_sponser_profile(sponser_id):
    if request.method=="POST":
        name=request.form.get("sponser_name")
        industry=request.form.get("industry")
        budget=request.form.get("budget")
        sponser=Sponser.query.filter_by(id=sponser_id).first()
        sponser.sponser_company_name=name
        sponser.Idustry=industry
        sponser.Budget=budget
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)



@app.route("/sponser_find/<int:sponser_id>",methods=["GET","POST"])
def sponser_search(sponser_id):
    all_influencers=Influencer.query.filter_by(flagged_status=0)
    if request.method=="POST":
        criteria=request.form.get("criteria")
        search=request.form.get("search")
        search =search.strip().lower()
        if criteria=="niche":
            influencers=Influencer.query.filter(func.lower(Influencer.niche).like(f"%{search}%")).all()
            if not influencers:
                influencers=Influencer.query.filter(func.lower(Influencer.category).like(f"%{search}%")).all()
            return render_template("sponser_find.html",sponser_id=sponser_id,influencers=influencers)
        else:
            reach=int(search)
            influencers = Influencer.query.filter(Influencer.reach > reach).all()
            return render_template("sponser_find.html",sponser_id=sponser_id,influencers=influencers)
    return render_template("sponser_find.html",sponser_id=sponser_id,all_influencers=all_influencers)


#routings for campaign management


@app.route("/sponser_campaign/<int:sponser_id>")
def sponser_campaigns(sponser_id):
    sponser = Sponser.query.get_or_404(sponser_id)
    all_campaigns=Campaign.query.filter_by(sponser_id=sponser_id,campaign_flagged_status=0).all()
    ad_requests=Ad_request.query.filter_by()
    all_influencers=Influencer.query.filter_by(flagged_status=0).all()
    return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)


@app.route("/add_campaign/<int:sponser_id>",methods=["GET","POST"])
def add_campaign(sponser_id):
    if request.method=="POST":
        c_name=request.form.get("campaign_name")
        visibility=int(request.form.get("visibility"))
        description=request.form.get("description")
        budget=int(request.form.get("budget"))
        s_date=request.form.get("start_date")
        e_date=request.form.get("end_date")
        noa=int(request.form.get("no_of_ads"))
        progress=int(request.form.get("progress"))
        goal=request.form.get("goal")
        niche=request.form.get("niche")
        existing_campaign=Campaign.query.filter_by(c_name=c_name,sponser_id=sponser_id).first()
        if existing_campaign:
             flash("campaign already exist! , try by some another name!!")
             sponser = Sponser.query.get_or_404(sponser_id)
             all_campaigns=Campaign.query.filter_by(sponser_id=sponser_id,campaign_flagged_status=0).all()
             all_influencers=Influencer.query.filter_by(flagged_status=0).all()
             return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)
        else:
            start_date_obj = datetime.strptime(s_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(e_date, '%Y-%m-%d').date()
            new_campaign=Campaign(c_name=c_name,visibility=visibility,description=description,budget=budget,start_date=start_date_obj,end_date=end_date_obj,no_of_ads=noa,progress=progress,goal=goal,sponser_id=sponser_id,niche=niche)
            db.session.add(new_campaign)
            db.session.commit()
            sponser = Sponser.query.get_or_404(sponser_id)
            all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
            all_influencers=Influencer.query.filter_by(flagged_status=0).all()
            return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)




@app.route("/edit_campaign/<int:sponser_id>",methods=["GET","POST"])
def edit_campaign(sponser_id):
    if request.method=="POST":
        campaign_id=request.form.get("campaign_id")
        c_name=request.form.get("campaign_name")
        visibility=int(request.form.get("visibility"))
        description=request.form.get("description")
        budget=int(request.form.get("budget"))
        s_date=request.form.get("start_date")
        e_date=request.form.get("end_date")
        noa=int(request.form.get("no_of_ads"))
        progress=int(request.form.get("progress"))
        goal=request.form.get("goal")
        niche=request.form.get("niche")
        sdate= datetime.strptime(s_date, '%Y-%m-%d').date()
        edate= datetime.strptime(e_date, '%Y-%m-%d').date()

        campaign=Campaign.query.filter_by(id=campaign_id).first()
        campaign.c_name=c_name
        campaign.visibility=visibility
        campaign.description=description
        campaign.budget=budget
        campaign.start_date=sdate
        campaign.end_date=edate
        campaign.no_of_ads=noa
        campaign.progress=progress
        campaign.goal=goal
        campaign.sponser_id=sponser_id
        campaign.niche=niche
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
        all_influencers=Influencer.query.filter_by(flagged_status=0).all()
        return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)
        # if existing_campaign:
        #      flash("campaign already exist! , try by some another name!!")
        #      return render_template("sponser_campaigns.html",sponser_id=sponser_id,campaigns=all_campaigns)
        # else:
        #     start_date_obj = datetime.strptime(s_date, '%Y-%m-%d').date()
        #     end_date_obj = datetime.strptime(e_date, '%Y-%m-%d').date()
        #     new_campaign=Campaign(c_name=c_name,visibility=visibility,description=description,budget=budget,start_date=start_date_obj,end_date=end_date_obj,no_of_ads=noa,progress=progress,goal=goal,sponser_id=sponser_id)
        #     db.session.add(new_campaign)
        #     db.session.commit()
        #     all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
        #     return render_template("sponser_campaigns.html",campaigns=all_campaigns,sponser_id=sponser_id)
    
    


    
@app.route("/delete_campaign/<int:sponser_id>",methods=["GET","POST"])
def delete_campaign(sponser_id):
    if request.method=="POST":
        campaign_id=request.form.get("campaign_id")
        campaign=Campaign.query.filter_by(id=campaign_id).first()
        db.session.query(Ad_request).filter(Ad_request.campaign_id == campaign_id).delete()
        db.session.delete(campaign)
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
        all_influencers=Influencer.query.filter_by(flagged_status=0).all()
        return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)

# Routings for sponser ad management for private campaigns

@app.route("/send_request/<int:sponser_id>",methods=["GET","POST"])
def add_request(sponser_id):
    if request.method=="POST":
        send_by=request.form.get("send_by")
        campaign_id=request.form.get("campaign_id")
        msg=request.form.get("msg")
        requirements=request.form.get("requirements")
        payment_amount=request.form.get("payment_amount")
        ad_request_status=request.form.get("status")
        influencer_id=request.form.get("influencer_id")
        existing_request=Ad_request.query.filter_by(influencer_id=influencer_id,campaign_id=campaign_id).first()
        if existing_request:
            flash("You already have send request to this influencer , try another one!!")
            sponser = Sponser.query.get_or_404(sponser_id)
            all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
            all_influencers=Influencer.query.filter_by(flagged_status=0).all()
            return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)
        else:
            new_request=Ad_request(send_by=0,msg=msg,requirements=requirements,payment_amount=payment_amount,influencer_id=influencer_id,campaign_id=campaign_id,sponser_id=sponser_id)
            db.session.add(new_request)
            db.session.commit()
            sponser = Sponser.query.get_or_404(sponser_id)
            all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
            all_influencers=Influencer.query.filter_by(flagged_status=0).all()
            return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)


@app.route("/modify_request/<int:sponser_id>",methods=["GET","POST"])
def modify_request(sponser_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        send_by=request.form.get("send_by")
        campaign_id=request.form.get("campaign_id")
        msg=request.form.get("msg")
        requirements=request.form.get("requirements")
        payment_amount=request.form.get("payment_amount")
        ad_request_status=request.form.get("status")
        influencer_id=request.form.get("influencer_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        if ad_request.ad_request_status=="accepted":
            pass
        else:
            ad_request.msg=msg
            ad_request.requirements=requirements
            ad_request.payment_amount=payment_amount
            ad_request.influencer_id=influencer_id
            db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
        all_influencers=Influencer.query.filter_by(flagged_status=0).all()
        return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers)


@app.route("/delete_request/<int:sponser_id>",methods=["GET","POST"])
def delete_request(sponser_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter(Ad_request.id==ad_id,Ad_request.ad_request_status!="accepted").first()
        if ad_request:
            db.session.delete(ad_request)
            db.session.commit()
            msg=""
        else:
            msg="You can not delete an ongoing campaign"
        sponser = Sponser.query.get_or_404(sponser_id)
        all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,sponser_id=sponser_id).all()
        all_influencers=Influencer.query.filter_by(flagged_status=0).all()
        return render_template("sponser_campaigns.html",sponser=sponser,sponser_id=sponser_id,campaigns=all_campaigns,influencers=all_influencers,msg=msg)


# sponser action routes for negotiation request that are send by influencer for private campaigns

@app.route("/accept_nego_ads/<int:sponser_id>",methods=["GET","POST"])
def accept_nego(sponser_id):
     if request.method=="POST":
        msg=request.form.get("msg")
        amount=request.form.get("payment_amount")
        ad_id=request.form.get("ad_id")
        campaign_id=request.form.get("campaign_id")
        nego_ads=Ad_request.query.filter_by(id=ad_id).first()
        nego_ads.nego=0
        nego_ads.msg=msg
        nego_ads.payment_amount=amount
        nego_ads.ad_request_status="accepted"
        campaign=Campaign.query.filter_by(id=campaign_id).first()
        campaign.campaign_status="accepted"
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)



@app.route("/reject_influ_nego/<int:sponser_id>",methods=["GET","POST"])
def reject_nego(sponser_id):
     if request.method=="POST":
        ad_id=request.form.get("ad_id")
        nego_ads=Ad_request.query.filter_by(id=ad_id).first()
        nego_ads.nego=1
        nego_ads.ad_request_status="rejected"
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)




# Routings for sponser ad request management for Public campaigns

@app.route("/sponser_negotiate_request/<int:sponser_id>",methods=["GET","POST"])         #send by influencer for public campaign , sponser send negotiation 
def negotiate_request(sponser_id):
    if request.method=="POST":
        msg=request.form.get("msg")
        amount=request.form.get("payment_amount")
        ad_id=request.form.get("ad_id")
        nego_ads=Ad_request.query.filter_by(id=ad_id,send_by=1).first()
        nego_ads.nego=1
        nego_ads.msg=msg
        nego_ads.payment_amount=amount
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)





@app.route("/influ_accept_ad_request/<int:sponser_id>",methods=["GET","POST"])
def accept_request(sponser_id):
    if request.method=="POST":
        campaign_id=request.form.get("campaign_id")
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        ad_request.ad_request_status="accepted"
        db.session.commit()
        campaign=Campaign.query.filter_by(id=campaign_id)
        campaign.campaign_status="accepted"
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)


@app.route("/influ_reject_ad_request/<int:sponser_id>",methods=["GET","POST"])
def reject_request(sponser_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        ad_request.ad_request_status="rejected"
        db.session.commit()
        sponser = Sponser.query.get_or_404(sponser_id)
        active_campaigns = Campaign.query.filter_by(sponser_id=sponser_id, campaign_flagged_status=0,campaign_status="accepted").all()
        newad_request= Ad_request.query.filter_by(send_by=1,nego=0,sponser_id=sponser_id, ad_request_status="pending").all()
        nego_ads=Ad_request.query.filter_by(nego=1,send_by=0,sponser_id=sponser_id).all()
        return render_template("sponser_dashboard.html", sponser=sponser, campaigns=active_campaigns, newads=newad_request,sponser_id=sponser_id,name=sponser.sponser_company_name,nego_ads=nego_ads)







# routes for influencer

@app.route("/influencer_dashboard/<int:influencer_id>")
def influencer_dashboard(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
    Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
    new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
    nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
    return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   

# search mechanism for influencer

@app.route("/influencer_find/<int:influencer_id>",methods=["GET","POST"])
def influencer_find(influencer_id):
    all_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    if request.method=="POST":
        criteria=request.form.get("criteria")
        search=request.form.get("search")
        search =search.strip().lower()
        if criteria=="all":
            return render_template("influencer_find.html",influencer_id=influencer_id,all_campaigns=all_campaigns)
        if criteria=="niche":
            campaigns=Campaign.query.filter(func.lower(Campaign.niche).like(f"%{search}%")).all()
            if campaigns:
                return render_template("influencer_find.html",influencer_id=influencer_id,campaigns=campaigns)
            else:
                msg="There are not any public campaign with this niche , try something else!!"
                return render_template("influencer_find.html",influencer_id=influencer_id,msg=msg)
        elif criteria=="budget":
            budget=int(search)
            campaigns=Campaign.query.filter(Campaign.budget > budget,Campaign.visibility==0).all()
            if campaigns:
                return render_template("influencer_find.html",influencer_id=influencer_id,campaigns=campaigns)
            else:
                msg="There are not any public campaign under this budget , try something else!!"
                return render_template("influencer_find.html",influencer_id=influencer_id,msg=msg)
    return render_template("influencer_find.html",influencer_id=influencer_id,all_campaigns=all_campaigns)



# progress update by influencer
@app.route("/progress_update/<int:influencer_id>",methods=["POST"])
def progress_update(influencer_id):
    if request.method=='POST':
        campaign_id=request.form.get("campaign_id")
        sponser_id=request.form.get("sponser_id")
        prg=int(request.form.get("progress"))
        campaign=Campaign.query.filter_by(id=campaign_id).first()
        total_ads = len(campaign.sponser_ads)
        progress=(campaign.progress)
        new_progress=(progress+int(prg/total_ads))
        campaign.progress=new_progress
        db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
# ad requests send by sponser for private campaigns , influencer sending negotiotion request

@app.route("/negotiate_request/<int:influencer_id>",methods=["GET","POST"])
def in_negotiate_request(influencer_id):
    if request.method=="POST":
        msg=request.form.get("msg")
        amount=request.form.get("payment_amount")
        ad_id=request.form.get("ad_id")
        nego_ads=Ad_request.query.filter_by(id=ad_id,send_by=0).first()
        nego_ads.nego=1
        nego_ads.msg=msg
        nego_ads.payment_amount=amount
        db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   

# ad requests send by sponser for private campaigns , influencer accepting request



@app.route("/accept_ad_request/<int:influencer_id>",methods=["GET","POST"])
def in_accept_request(influencer_id):
    if request.method=="POST":
        campaign_id=request.form.get("campaign_id")
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        campaign=Campaign.query.filter_by(id=campaign_id).first()
        campaign.campaign_status="accepted"
        ad_request.ad_request_status="accepted"
        ad_request.nego=0
        db.session.commit()
        
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
# ad requests send by sponser for private campaigns , influencer rejecting request


@app.route("/reject_ad_request/<int:influencer_id>",methods=["GET","POST"])
def in_reject_request(influencer_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        ad_request.ad_request_status="rejected"
        db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
# ad requests send by influencer for public campaigns 
@app.route("/send_ad_request/<int:influencer_id>",methods=["GET","POST"])
def influencer_add_request(influencer_id):
     if request.method=="POST":
        send_by=request.form.get("send_by")
        campaign_id=request.form.get("campaign_id")
        sponser_id=request.form.get("sponser_id")
        msg=request.form.get("msg")
        requirements=request.form.get("requirements")
        payment_amount=request.form.get("payment_amount")
        existing_request=Ad_request.query.filter_by(influencer_id=influencer_id,campaign_id=campaign_id,send_by=1).first()
        if existing_request:
            msg="You already have send request to this campaign , try another one!!"
            influencer = Influencer.query.get_or_404(influencer_id)
            accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
            Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
            new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
            nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
            return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
        else:
            new_request=Ad_request(send_by=1,msg=msg,requirements=requirements,payment_amount=payment_amount,influencer_id=influencer_id,campaign_id=campaign_id,sponser_id=sponser_id)
            db.session.add(new_request)
            db.session.commit()
            influencer = Influencer.query.get_or_404(influencer_id)
            accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
            Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
            new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
            nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
            return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   


@app.route("/modify_ad_request/<int:influencer_id>",methods=["GET","POST"])
def modify_influencer_ad_request(influencer_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        send_by=request.form.get("send_by")
        campaign_id=request.form.get("campaign_id")
        msg=request.form.get("msg")
        requirements=request.form.get("requirements")
        payment_amount=request.form.get("payment_amount")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        if ad_request.ad_request_status=="accepted":
            pass
        else:
            ad_request.msg=msg
            ad_request.requirements=requirements
            ad_request.payment_amount=payment_amount
            ad_request.influencer_id=influencer_id
            db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   

@app.route("/delete_ad_request/<int:influencer_id>",methods=["GET","POST"])
def delete_influencer_ad_request(influencer_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter(Ad_request.id==ad_id,Ad_request.ad_request_status!="accepted").first()
        if ad_request:
            db.session.delete(ad_request)
            db.session.commit()
            msg=""
        else:
            msg="You can not delete an ongoing campaign"
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
@app.route("/influencer_profile/<int:influencer_id>")
def influencer_profile(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    return render_template("influencer_profile.html",i_user=influencer)


@app.route("/update_influencer_profile/<int:influencer_id>",methods=["GET","POST"])
def update_influencer_profile(influencer_id):
    if request.method=="POST":
        name=request.method.get("influencer_name")
        reach=request.method.get("reach")
        niche=request.method.get("niche")
        influencer=Influencer.query.filter_by(id=influencer_id).first()
        influencer.name=name
        influencer.reach=reach
        influencer.niche=niche
        db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   
# Influencer response for negotiation requests send by sponser for public campaign
# accept

@app.route("/spon_accept_ad_request/<int:influencer_id>",methods=["GET","POST"])
def spon_accept_request(influencer_id):
    if request.method=="POST":
        campaign_id=request.form.get("campaign_id")
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        campaign=Campaign.query.filter_by(id=campaign_id).first()
        campaign.campaign_status="accepted"
        ad_request.ad_request_status="accepted"
        ad_request.nego=0
        db.session.commit()
        
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
     
# reject


@app.route("/spon_reject_ad_request/<int:influencer_id>",methods=["GET","POST"])
def spon_reject_request(influencer_id):
    if request.method=="POST":
        ad_id=request.form.get("ad_id")
        ad_request=Ad_request.query.filter_by(id=ad_id).first()
        ad_request.ad_request_status="rejected"
        db.session.commit()
        influencer = Influencer.query.get_or_404(influencer_id)
        accepted_campaigns = Campaign.query.join(Campaign.sponser_ads).filter(Ad_request.ad_request_status == "accepted",Ad_request.influencer_id == influencer_id).all()
        Requested_ads=Ad_request.query.filter_by(send_by=1,influencer_id=influencer_id,nego=0,ad_request_status="pending").all()
        new_ad_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0,nego=0).all()
        nego_requests=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=1,nego=1).all()
        return render_template("influencer_dashboard.html",name=influencer.influencer_name,influencer_id=influencer_id,campaigns=accepted_campaigns,newads=new_ad_requests,requested_ads=Requested_ads,nego_requests=nego_requests,i_user=influencer)
   

def Insc_summary():
    campaigns=Campaign.query.all()
    sponsers=Sponser.query.all()
    influencers=Influencer.query.all()
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    ad_request=Ad_request.query.all() 
    accepted_requests = Ad_request.query.filter_by(ad_request_status="accepted").all()
    rejected_requests = Ad_request.query.filter_by(ad_request_status="rejected").all()
    pending_requests = Ad_request.query.filter_by(ad_request_status="pending").all()

    pb_count = len(active_pb_campaigns) or 0
    pr_count = len(active_pr_campaigns) or 0
    fc_count = len(flagged_campaigns) or 0
    asp_count = len(active_sponsers) or 0
    fs_count = len(flagged_sponsers) or 0
    ai_count = len(active_influencers) or 0
    fi_count = len(flagged_influencers) or 0
    tar_count = len(ad_request) or 0
    ar_count = len(accepted_requests) or 0
    rr_count = len(rejected_requests) or 0
    pr_count = len(pending_requests) or 0
    path="static/img/summaries/"
    if campaigns:
        plt.title("Campaign Summary")
        Data = [pb_count, pr_count,fc_count]
        labels = ["Public campaign", "Private Campaign", "Flagged campaign"]
        plt.bar(labels,Data,width=0.3,color="green")
        plt.savefig(path+"campaign.jpg")
        plt.clf()
    
    if sponsers:
        Data = [asp_count, fs_count]
        labels = ["Active Sponsor", "Flagged Sponsor"] 
        plt.title("Sponser Summary")
        plt.bar(labels,Data,width=0.3,color="red")
        plt.savefig(path+"sponser.jpg")
        plt.clf()
   
    if influencers:
        Data = [ai_count, fi_count]
        labels = ["Active Influencer", "Flagged Influencer"] 
        plt.title("Influencer Summary")
        plt.bar(labels,Data,width=0.3,color="maroon")
        plt.savefig(path+"influencer.jpg")
        plt.clf()
    if ad_request:
        Data = [pr_count,ar_count,rr_count]
        labels = ["Pending Ad_rewuestr", "Accepted Ad Request","Rejected Ad_request"] 
        plt.title("Ad Request Summary")
        plt.bar(labels,Data,width=0.3,color="maroon")
        plt.savefig(path+"ad_request.jpg")
        plt.clf()


@app.route("/admin_stat")
def stats():
    campaigns=Campaign.query.all()
    sponsers=Sponser.query.all()
    influencers=Influencer.query.all()
    active_pb_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=0).all()
    active_pr_campaigns=Campaign.query.filter_by(campaign_flagged_status=0,visibility=1).all()
    flagged_campaigns=Campaign.query.filter_by(campaign_flagged_status=1).all()
    active_sponsers=Sponser.query.filter_by(flagged_status=0).all()
    flagged_sponsers=Sponser.query.filter_by(flagged_status=1).all()
    active_influencers=Influencer.query.filter_by(flagged_status=0).all()
    flagged_influencers=Influencer.query.filter_by(flagged_status=1).all()
    ad_request=Ad_request.query.all() 
    accepted_requests = Ad_request.query.filter_by(ad_request_status="accepted").all()
    rejected_requests = Ad_request.query.filter_by(ad_request_status="rejected").all()
    pending_requests = Ad_request.query.filter_by(ad_request_status="pending").all()
    return render_template("insc_platform_summary.html",total_sponsers=sponsers,total_influencer=influencers,pb_campaigns=active_pb_campaigns,pr_campaigns=active_pr_campaigns,flagged_campaigns=flagged_campaigns,total_campaigns=campaigns,active_sponsers=active_sponsers,flagged_sponsers=flagged_sponsers,active_influencers=active_influencers,flagged_influencers=flagged_influencers,TAR=ad_request)

@app.route("/sponser_summary/<int:sponser_id>")
def sponser_chart(sponser_id):
    campaigns=Campaign.query.filter_by(sponser_id=sponser_id).all()
    acampaigns=Campaign.query.filter_by(sponser_id=sponser_id,campaign_status="accepted").all()
    pcampaigns=Campaign.query.filter_by(sponser_id=sponser_id,campaign_status="pending").all()
    tc=len(campaigns) or 0
    ac=len(acampaigns) or 0
    pc=len(pcampaigns) or 0
    path="static/img/summaries/"
    if campaigns:
        plt.title("Campaign Summary")
        Data = [tc,ac,pc]
        labels = ["Total campaign", "Accepted Campaign", "Pending campaign"]
        plt.bar(labels,Data,width=0.3,color="green")
        plt.savefig(path+"sponsercampaign.jpg")
        plt.clf()
    return render_template("sponser_summary.html",sponser_id=sponser_id,campaigns=campaigns)


@app.route("/influencer_summary/<int:influencer_id>")
def influencer_chart(influencer_id):
    Ads=Ad_request.query.filter_by(influencer_id=influencer_id).all()
    accepted_ad_request=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="accepted",send_by=0).all()
    pending_ad_request=Ad_request.query.filter_by(influencer_id=influencer_id,ad_request_status="pending",send_by=0).all()
    aa=len(accepted_ad_request) or 0
    pa=len(pending_ad_request) or 0
    path="static/img/summaries/"
    if Ads:
        plt.title("Ad Request Summary")
        Data = [aa,pa]
        labels = ["Accepted Ad Request", "Pending Ad Request"]
        plt.bar(labels,Data,width=0.3,color="green")
        plt.savefig(path+"influencerads.jpg")
        plt.clf()

    return render_template("influencer_summary.html",influencer_id=influencer_id,ads=Ads)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")