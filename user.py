from flask import *
from database import *
import uuid
user=Blueprint("user",__name__)


@user.route("/userhome")
def userhome():
    return render_template("userhome.html")

@user.route('/user_view_company',methods=['get','post'])
def viewcompany():
    data={}
    s="select * from company"
    se=select(s)
    print(se)
    data['key']=se

    return render_template('user_view_company.html',data=data)

@user.route('/user_view_job',methods=['get','post'])
def viewjobs():
    id=request.args['id']
    data={}
    s="select * from jobs where company_id='%s'"%(id)
    se=select(s)
    print(se)
    data['key']=se

    return render_template('user_view_job.html',data=data)

@user.route('/application_req',methods=['get','post'])
def application_req():
    id=request.args['id']
    if 'submit' in request.form:
        date=request.form['date']
       
        y="insert into application_request values(null,'%s','%s','%s','pending')"%(id,session['uid'],date)
        insert(y)
        return redirect(url_for('user.view_my_application'))
    return render_template("application_req.html")



@user.route("/user_view_mark",methods=['get','post'])
def user_view_mark():
    # uid=request.args['uid']
    data={}
    s="select * from answers where user_id='%s'"%(session['uid'])
    data["key"]=select(s)

    return render_template('user_view_mark.html',data=data)


@user.route("/view_my_application",methods=['get','post'])
def view_my_application():

    
    data={}
    se="select * from application_request inner join jobs using(job_id) inner join user using(user_id) where login_id='%s'"%(session['lid'])
    print(se)
    s=select(se)
    print(s,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    data['key']=s
    # return redirect(url_for(user.))
    return render_template('view_my_application.html',data=data)


@user.route("/view_my_profile",methods=['get','post'])
def view_my_profile():

    
    data={}
    se="select * from user inner join personal_details using(user_id) where login_id='%s'"%(session['lid'])
    print(se)
    s=select(se)
    print(s)
    data['key']=s
    return render_template('view_my_profile.html',data=data)

@user.route("/instruction",methods=['get','post'])
def instruction():

     data={}
     se="select * from application_request inner join jobs using(job_id) inner join user using(user_id) where login_id='%s'"%(session['lid'])
     print(se)
     s=select(se)
     data['key']=s
     return render_template('instruction.html',data=data)



@user.route("/user_update_profile",methods=['get','post'])
def user_update_profile():
    data={}
    d="select * from user inner join personal_details using(user_id) where login_id='%s'"%(session['lid'])
   
    s=select(d)
    print("_____",s)
    data['key']=s
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
        print(fname,lname,address,place,phone,email,gender,pincode)
        u="update user set first_name='%s',last_name='%s',place='%s',phone='%s',email='%s',gender='%s',pincode='%s'"%(fname,lname,place,phone,email,gender,pincode)
        update(u)
        v="update personal_details set full_name='%s',address='%s',skills='%s',work_experience='%s',company_name='%s',job_role='%s',current_ctc='%s',expected_ctc='%s',suggested_role='%s'"%(fname,address,skills,we,company,job_role,current_ctc,expected_ctc,suggested_role)
        update(v)
        return '''<script>alert('Updated');window.location='/view_my_profile';</script>'''

        # return redirect(url_for("user.view_my_profile"))
    return render_template('user_update_profile.html',data=data)


from sample import *
from em import *
from threading import Event
import threading

@user.route('/start_test',methods=['get','post'])
def start_test():
    import cv2
    import mediapipe as mp
    import numpy as np
    

    import threading
    rid=request.args['rid']
    aid=request.args['aid']
    cid=request.args['cid']
    # r="select * from application_request where request_id='%s'"%(rid)
    # res=select(r)
    # ans_id=res[0]['answer_id']
    a="select * from apti_answers where answer_id='%s'"%(aid)
    res=select(a)
    eid=res[0]['experience_type_id']
    jid=res[0]['job_role_id']
    # jobid=request.args['job_id']
    data={}
    uid=session['uid']
    print("____________________________________eid_____",eid)
    print("___________________jid_____________",jid)
    print("______________________________cid__________",cid)
    c="select * from company where login_id='%s'"%(cid)
    resc=select(c)
    coid=cid

    s="select * from answers where experience_type_id='%s' and job_role_id='%s' and user_id='%s'"%(rid,jid,uid)
    res=select(s)
    if not res:
        
        # cid=request.args['cid']

        # stop_camera_event.clear()
        # camera_thread = threading.Thread(target=detection, args=(uid,))
        # camera_thread.start()
        print("_________________eid_____",eid,jid,coid)
        d="select * from online_test where experience_type_id='%s' and job_role_id='%s' and company_id='%s'"%(eid,jid,coid)
        data['view']=select(d)
        re=select(d)
        print("exm wn__________________",re)

        if not re:
            return '''<script>alert("No Data");window.location='/view_my_application'</script>'''

        if re:
            stop_camera_event.clear()
            camera_thread = threading.Thread(target=detection, args=(uid,cid,))
            camera_thread.start()

            if "submit" in request.form:
                stop_camera_event.set() 
                
                # camera_thread.join()
                # global camera_running
                # camera_running = False
                print("_________________ZFDSFSDF")

                j=1
                a=0
                counter = 0
                for i in data['view']:
                    counter += 1
                    radio=request.form["ans"+str(j)]
                    if i['correct_option']==radio:
                        a=a+1
                        
                    j=j+1
                print(a,counter)
                print("^^^^^^^^^^^^^^^^^^^^^^^^mark^^^^^^",a)
                
                qry="insert into answers values(null,'%s','%s','%s','%s','%s',curdate(),'%s')"%(eid,uid,jid,a,counter,rid)
                session['ansid']=insert(qry)
                u="update application_request set req_status='exam attended' where request_id='%s'"%(rid)
                update(u)
                # x="select * from application_request where user_id='%s' and job_id='%s'"%(uid,jobid)
                # xr=select(x)
                # if xr:
                #     q = "SELECT * FROM `answers` WHERE user_id='%s' and experience_type_id='%s' and job_role_id='%s'" % (uid,eid,jid)
                #     print(q)
                #     res = select(q)
                #     point = res[0]['mark_awarded']
                #     u="update application_request set req_status='mark : %s' where user_id='%s' and company_id='%s'"%(point,uid,cid)
                #     update(u)
                    
                    
                
                return redirect(url_for('user.user_view_mark'))
        
        

            return render_template('start_test.html',data=data)
    else:
        # flash('You Already Taken The Test')
        return '''<script>alert("You Already Taken The Test");window.location='/view_my_application'</script>'''
        # return redirect(url_for('userviewcompanies'))
    

# @user.route("/jobsearch",methods=['get','post'])
# def jobsearch():
#     data={}
#     s="select * from experience_type"
#     se=select(s)
#     print(se)
#     data['key']=se
#     j="select * from job_role"
#     data['job']=select(j)
#     if "submit" in request.form:
#         etype=session['etype']=request.form['etype']
#         jrole=session['jrole']=request.form['jrole']
#         qry = "select * from apti_test where experience_type_id='%s' and job_role_id='%s' ORDER BY RAND() LIMIT 10" % (etype,jrole)
#         rs=select(qry)
#         data['res1']=session['res1'] = select(qry)
#         print("____________________",rs)
#         # return '''<script>window.location='/search_job_aptitude';alert("Start test...")</script>'''
#         return render_template('search_job_aptitude.html',data=data)


#     return render_template('jobsearch.html',data=data)
#     # return redirect(url_for('search_job_aptitude'))



# @user.route("/search_job_aptitude",methods=['get','post'])
# def search_job_aptitude():
#     print("vannuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
#     if "answer" in request.form:
#         print("*******************************************")
        
#         j=1
#         a=0
#         counter = 0
#         for i in session['res1']:
#             counter += 1
#             radio=request.form["ans"+str(j)]
#             if i['correct_option']==radio:
#                 a=a+1
#             j=j+1
#         print(a,counter)
        
#         qry="insert into apti_answers values(null,'%s','%s','%s','%s','%s',curdate())"%(session['etype'],session['jrole'],session['uid'],a,counter)
        
#         session['ansid']=insert(qry)
#         print("+++++++++++++++++++++++++++++++++++++",type(a))

#         if a>=2:
#             # flash(f"Eligible with a score of {a}")
#             return '''<script>window.location='/user_view_jobs';alert("eligible")</script>'''

#             # return redirect(url_for('user.user_view_jobs'))
#         else:
#             return '''<script>window.location='/search_job_aptitude';alert("Not eligible ")</script>'''
#             # return redirect(url_for('user.search_job_aptitude'))

#     return render_template('search_job_aptitude.html')
    
@user.route("/search_job_aptitude",methods=['get','post'])
def search_job_aptitude():
    data={}
    s="select * from experience_type"
    se=select(s)
    print(se)
    data['key']=se
    j="select * from job_role"
    data['job']=select(j)
    if "submit" in request.form:
        etype=session['etype']=request.form['etype']
        jrole=session['jrole']=request.form['jrole']
        qry = "select * from apti_test where experience_type_id='%s' and job_role_id='%s' ORDER BY RAND() LIMIT 10" % (etype,jrole)
        rs=select(qry)
        data['res1']=session['res1'] = select(qry)
    
        print("____________________",rs)
        if not rs:
            return '''<script>window.location='/search_job_aptitude';alert("No Data ")</script>'''

    if "answer" in request.form:
        print("*******************************************")
        
        j=1
        a=0
        counter = 0
        for i in session['res1']:
            counter += 1
            radio=request.form["ans"+str(j)]
            if i['correct_option']==radio:
                a=a+1
            j=j+1
        print(a,counter)
        
        qry="insert into apti_answers values(null,'%s','%s','%s','%s','%s',curdate())"%(session['etype'],session['jrole'],session['uid'],a,counter)
        
        session['ansid']=insert(qry)
        print("+++++++++++++++++++++++++++++++++++++",type(a))

        if a>=5:
            return '''<script>window.location='/user_view_jobs';alert("eligible")</script>'''

            return redirect(url_for('user.user_view_jobs'))
        else:
            return '''<script>window.location='/search_job_aptitude';alert("Not eligible ")</script>'''
            return redirect(url_for('user.search_job_aptitude'))
        

    return render_template('search_job_aptitude.html',data=data)

    
# @user.route("/search_job_aptitude",methods=['get','post'])
# def search_job_aptitude():
#     data={}
#     s="select * from experience_type"
#     se=select(s)
#     print(se)
#     data['key']=se
#     j="select * from job_role"
#     data['job']=select(j)
#     if "submit" in request.form:
#         etype=session['etype']=request.form['etype']
#         jrole=session['jrole']=request.form['jrole']
#         qry = "select * from apti_test where experience_type_id='%s' and job_role_id='%s' ORDER BY RAND() LIMIT 10" % (etype,jrole)
#         rs=select(qry)
#         data['res1']=session['res1'] = select(qry)
    
#         print("____________________",rs)
#     if "answer" in request.form:
#         print("*******************************************")
        
#         j=1
#         a=0
#         counter = 0
#         for i in session['res1']:
#             counter += 1
#             radio=request.form["ans"+str(j)]
#             if i['correct_option']==radio:
#                 a=a+1
#             j=j+1
#         print(a,counter)
        
#         qry="insert into apti_answers values(null,'%s','%s','%s','%s','%s',curdate())"%(session['etype'],session['jrole'],session['uid'],a,counter)
        
#         session['ansid']=insert(qry)
#         print("+++++++++++++++++++++++++++++++++++++",type(a))

#         if a>=2:
#             # flash(f"Eligible with a score of {a}")
#             return '''<script>window.location='/user_view_jobs';alert("eligible")</script>'''

#             # return redirect(url_for('user.user_view_jobs'))
#         else:
#             return '''<script>window.location='/search_job_aptitude';alert("Not eligible ")</script>'''
#             # return redirect(url_for('user.search_job_aptitude'))

#     return render_template('search_job_aptitude.html',data=data)



import re
@user.route('/user_view_jobs')
def user_view_jobs():
    # import fitz
    data={}
    query = "select * from personal_details inner join user using(user_id) where user_id='%s'" % (session['uid'])
    res = select(query)
    print("__________res___________",res)
        
    # Convert each dictionary to a formatted string
    formatted_strings = [f"{', '.join([f'{key}={value}' for key, value in d.items()])}" for d in res]

    # Join the formatted strings with newline or any separator
    result_string = '\n'.join(formatted_strings)

    # Preprocessing and matching skills
    # skills = ['Python', 'Java', 'SQL', 'Data Analysis']
    resume_text = result_string
    # resume_text = 'I am a Python developer with experience in SQL and data analysis.'

    # Preprocessing
    resume_text = re.sub(r'[^\w\s]','',resume_text) # Remove punctuation	
    resume_text = resume_text.lower() # Convert to lowercase
    print("____________resume_______________",resume_text)

    q = "SELECT * FROM `jobs` inner join company using(company_id)"
    result = select(q)

    # Initialize an empty list to store the individual skills
    all_skills = []
    output=[]
    # Iterate through each dictionary in the 'result' list
    for c_skill in result:
        all_skills = []

        # Split the details string into a list using ','
        details_list = c_skill['details'].split(',')

        # Create a generator expression to strip whitespaces from each skill
        stripped_skills_generator = (skill.strip() for skill in details_list)
        # Extend the all_skills list with the stripped skills
        all_skills.extend(stripped_skills_generator)



        # Matching skills
        matches = [skill for skill in all_skills if re.search(skill.lower(), resume_text)]
        print('matches____________________________________',matches)
        # Scoring matches
        score = len(matches)
        print("score : ", score)
        matched_job_vacancies=""

        # Filtering resumes
        threshold = 1 # Set threshold for matches
        if score > threshold:
            output.append(c_skill)

        else:
            print('Resume does not match')
    

    data['job']=output

    print("output___________________",output)
    return render_template('upload_pdf.html',data=data)

@user.route("/send_feedback",methods=['get','post'])
def send_feedback():
    data={}
    d="select * from complaint where user_id='%s'"%(session['uid'])
    data['key']=select(d)
    if 'submit' in request.form:
        comp=request.form['comp'] 
    
        q="insert into complaint values(null,'%s','pending','%s',curdate())"%(comp,session['uid'])
        insert(q)
        return '''<script>alert("Send");window.location='/send_feedback'</script>'''

    return render_template("send_feedback.html",data=data)


@user.route('/usersendapplication', methods=['GET', 'POST'])
def usersendapplication():
    if "job_id" in request.args:
        session['job_id'] = request.args['job_id']
        session['company_id']=cid = request.args['company_id']
    data = {}

    # sid = session['id']

    q = "SELECT * FROM application_request WHERE user_id='%s' AND job_id='%s'" % (session['uid'], session['job_id'])
    res = select(q)
    # print(sid)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    if res:
        flash("YOU ALREADY REQUESTED")
        return '''<script>window.location='/user_view_jobs';alert('YOU ALREADY REQUESTED');</script>'''
        return redirect(url_for('user.user_view_jobs'))

    if not res:
        q="insert into application_request values(null,'%s','%s',curdate(),'pending','%s')"%(session['job_id'],session['uid'],session['ansid'])
        # q = "INSERT INTO application VALUES (null,'%s''%s',curdate(),,'applied')" % (
        # session['id'], path, prediction, point, session['job_id'], session['company_id'])
        insert(q)
        flash('send successfully')
    return '''<script>window.location='/user_view_jobs';alert('application send');</script>'''

@user.route('/rate_us',methods=['post','get'])
def rate_us():
    if 'submit' in request.form:
        rate=request.form['rat']
        review=request.form['rev']
        
        q="select * from rating where user_id='%s'"%(session['uid'])
        r=select(q)
        if r:
            return '''<script>alert("Already rated");window.location="/us_pay_history"</script>'''
        else:

            
            qry="insert into rating values(null,'%s','%s','%s',curdate())"%(session['uid'],rate,review)
            insert(qry)
            return '''<script>alert("rating send successfully");window.location="/userhome"</script>'''
    return render_template('rate_us.html')

