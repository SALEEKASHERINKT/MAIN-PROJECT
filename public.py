import os
import uuid
from flask import *
from core import enf
from database import *
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse

public=Blueprint('public',__name__)

@public.route('/')
def home():  
      
    return render_template('home.html')

@public.route('/public_view_jobs', methods=['GET', 'POST'])
def scrape_jobs():
    if request.method == 'POST':
        # Get user inputs from the form
        keyword = request.form['keyword']
        location = request.form['location']
        print("++++++++++++++++++",keyword,location)

        # Call the web scraping function
        job_listings = scrape_linkedin(keyword, location)
        print("____________________________________",job_listings)
       

        # Render the template with the job listings
        return render_template('public_jobs.html', jobs=job_listings)

    # Render the initial form
    return render_template('public_job.html')

def scrape_linkedin(keyword, location):
    l = []
    k = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    # target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=100293800&currentJobId=3415227738&start={}'
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=102713980&currentJobId=3415227738&start={}'  # working - Chennai, India
    # target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=101282230&currentJobId=3415227738&start={}'  # working - London, UK


    # Replace the placeholders with the user inputs
    target_url = target_url.format(keyword.replace(" ", "%20"), location.replace(" ", "%20"), "{}")

    for i in range(0, math.ceil(117 / 25)):
        res = requests.get(target_url.format(i * 25))
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")
        print(len(alljobs_on_this_page))

        for x in range(0, len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)

    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

    for j in range(0, len(l)):
        resp = requests.get(target_url.format(l[j]))
        soup = BeautifulSoup(resp.text, 'html.parser')
        o = {}  # Initialize the dictionary for each iteration

        try:
            o["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            pass  # Skip this entry if company name is not found

        try:
            o["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            pass  # Skip this entry if job title is not found

        try:
            o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace("Seniority level", "").strip()
        except:
            pass  # Skip this entry if job level is not found

        try:
            o["job-description"] = soup.find("div", {"class": "show-more-less-html__markup"}).text.strip()
        except:
            pass  # Skip this entry if job description is not found

        if o:  # Only append non-empty dictionaries
            k.append(o)

    return k


@public.route('/login',methods=['get','post'])
def login(): 
    if 'submit' in request.form:
        uname=request.form['uname'] 
        pasw=request.form['pasw']
        
        qry="select * from login where username='%s' and password='%s'"%(uname,pasw)
        a=select(qry)
        if a:
            utype=a[0]['usertype']
            session['lid']=a[0]['login_id']
            if utype=='admin':
                return redirect(url_for('admin.adminhome'))
            elif utype=='user':
                a="select * from user where login_id='%s'"%(session['lid'])
                b=select(a)
                if b:
                    session['uid']=b[0]['user_id']
                    return redirect(url_for('user.userhome'))
            elif utype=='company':
                q="select * from company where login_id='%s'"%(session['lid'])
                r=select(q)
                if r:
                    session['cid']=r[0]['company_id']
                    return redirect(url_for('company.companyhome'))

    return render_template('login.html')
# @public.route('/u_reg',methods=['get','post'])
# def u_reg():
#     data={}
#     if 'submit' in request.form:
#         fname=request.form['fname']
#         lname=request.form['lname']
#         address=request.form['address']
#         place=request.form['place']
#         phone=request.form['phn']
#         email=request.form['email']
#         gender=request.form['gender']
#         pincode=request.form['pincode']
#         skills=request.form['skills']
#         we=request.form['work_experience']
#         company=request.form['company_name']
#         job_role=request.form['job_role']
#         current_ctc=request.form['current_ctc']
#         expected_ctc=request.form['expected_ctc']
#         suggested_role=request.form['suggested_role']
#         uname=request.form['uname'] 
#         pasw=request.form['pasw']
        
#         q="insert into login values(null,'%s','%s','user')"%(uname,pasw)
#         id=insert(q)
        
#         c="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id,fname,lname,address,place,phone,email,gender,pincode)
#         cd=insert(c)

#         d="insert into personal_details values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(cd,fname,lname,address,skills,we,company,job_role,current_ctc,expected_ctc,suggested_role)
#         insert(d)

#         # return redirect(url_for("login"))

#     return render_template('u_reg.html',data=data)

@public.route('/u_reg',methods=['get','post'])
def u_reg():
    data={}
    if 'submit' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        address=request.form['address']
        place=request.form['place']
        phone=request.form['phn']
        email=request.form['email']
        gender=request.form['gender']
        pincode=request.form['pincode']
        skills=request.form['skills']
        we=request.form['work_experience']
        company=request.form['company_name']
        job_role=request.form['job_role']
        current_ctc=request.form['current_ctc']
        expected_ctc=request.form['expected_ctc']
        suggested_role=request.form['suggested_role']
        uname=request.form['uname'] 
        pasw=request.form['pasw']
        
        
        q="insert into login values(null,'%s','%s','user')"%(uname,pasw)
        id=insert(q)
        
        c="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email,gender,pincode)
        cd=insert(c)

        d="insert into personal_details values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fname,address,skills,we,company,job_role,current_ctc,expected_ctc,suggested_role,cd)
        insert(d)
        pid=str(cd)
        isFile = os.path.isdir("static/trainimages/"+pid)  
        print(isFile)
        if(isFile==False):
            os.mkdir('static/trainimages/'+pid)
        image1=request.files['img1']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image1.filename
        image1.save(path)

        image2=request.files['img2']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image2.filename
        image2.save(path)

        image3=request.files['img3']
        path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image3.filename
        image3.save(path)
        enf("static/trainimages/")
        print("________________okkk___________")
        flash('Added successfully...')
        return '''<script>window.location="/";alert("Successfully Registered")</script>'''


        # return redirect(url_for("public.u_reg"))

    return render_template('u_reg.html',data=data)
@public.route('/c_reg',methods=['get','post'])
def c_reg():
    if 'submit' in request.form:
       
        cname=request.form['cname']
        plc=request.form['plc']
        phone=request.form['phone']
        e_mail=request.form['e_mail']
        est_yr=request.form['est_yr']
        uname=request.form['uname'] 
        pasw=request.form['pasw']
        file=request.files['image']
        path='static/'+str(uuid.uuid4())+file.filename
        file.save(path)
        website=request.form['website']
        latitude=request.form['latitude']
        longitude=request.form['longitude']
        
        c="insert into login values(null,'%s','%s','pending')"%(uname,pasw)
        a=insert(c)

        com="insert into company values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(a,path,cname,plc,phone,e_mail,est_yr,website,longitude,latitude)
        insert(com)
        return '''<script>window.location="/";alert("Successfully Registered")</script>'''
    return render_template('c_reg.html')




