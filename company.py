from flask import *
from database import *
company=Blueprint("company",__name__)


@company.route("/companyhome")
def companyhome():
    return render_template("companyhome.html")


@company.route("/uploadjob",methods=['get','post'])
def uploadjob():
    if 'submit' in request.form:

        jobtitle=request.form['jobtitle']
        qualification=request.form['qualification']
        details=request.form['details']
        lastdate=request.form['lastdate']
        date=request.form['date']

        x="insert into jobs values(null,'%s','%s','%s','%s','%s','%s','pending')"%(session['cid'],jobtitle,qualification,details,lastdate,date)
        insert(x)
    
    return render_template("jobs.html")
   
@company.route("/view_application",methods=['get','post'])
def view_application():
    
    data={}
    se="select * from application_request inner join jobs using(job_id) inner join user using(user_id)"
    print(se)
    s=select(se)
    data['key']=s
    return render_template('view_application.html',data=data)

@company.route('/company_View_application',methods=['get','post'])
def company_view_application():
	data={}
	jid=request.args['jid']
	se="select * from application_request inner join user using(user_id) inner join personal_details using(user_id) inner join jobs using(job_id) where company_id='%s'and job_id='%s'"%(session['cid'],jid)
	print(se)
	s=select(se)
	data['key']=s
	return render_template('view_application.html',data=data)


@company.route('/add_online_test',methods=['get','post'])
def online_test():
    data={}
    v="select * from online_test inner join experience_type using(experience_type_id) inner join job_role using(job_role_id) where company_id='%s'"%(session['cid'])
    data['apt']=select(v)
    s="select * from job_role"
    se=select(s)
    print(se)
    data['key']=se
    a="select * from experience_type"
    data['value']=select(a)

    if 'submit' in request.form:
        experience_type=request.form['experience_type']
        job_role=request.form['job_role']
        ques=request.form['ques']
        opt1=request.form['opt1']
        opt2=request.form['opt2']
        opt3=request.form['opt3']
        opt4=request.form['opt4']
        crt_opt=request.form['crt_opt']
        
        q="insert into online_test values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(experience_type,session['cid'],job_role,ques,opt1,opt2,opt3,opt4,crt_opt)
        id=insert(q)
        return(redirect(url_for("company.online_test")))
    return render_template('add_online_test.html',data=data)
    
@company.route('/company_accept_application')
def company_accept_application():
    rid=request.args['rid']
    u="update application_request set req_status='accept' where request_id='%s'"%(rid)
    update(u)
    return '''<script>window.location='/companyhome';alert('accept');</script>'''


@company.route('/company_reject_application')
def company_reject_application():
    rid=request.args['rid']
    u="delete from application_request where request_id='%s'"%(rid)
    delete(u)
    return '''<script>window.location='/companyhome';alert('reject');</script>'''


@company.route("/company_view_mark")
def company_view_mark():
    rid=request.args['rid']
    data={}
    s="select * from answers where request_id='%s'"%(rid)
    data["view"]=select(s)

    return render_template('company_view_mark.html',data=data)

@company.route("/com_view_malpractice")
def company_view_malpractice():
    data={}
    d="select * from malpractice inner join user using (user_id) where company_id='%s'"%(session['cid'])
    data["view"]=select(d)

    return render_template('com_view_malpractice.html',data=data)

@company.route('/company_proceed_selection')
def company_proceed_selection():
    rid=request.args['rid']
    u="update application_request set req_status= 'selected' where request_id='%s'"%(rid)
    update(u)
    return '''<script>window.location='/companyhome';alert('Proceeded Successfully');</script>'''

@company.route('/company_reject_selection')
def company_reject_selection():
    rid=request.args['rid']
    u="update application_request set req_status='rejected' where request_id='%s'"%(rid)
    update(u)
    return '''<script>window.location='/companyhome';alert('Selection Rejected');</script>'''


@company.route('/company_manage_job',methods=['get','post'])
def company_Manage_job():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM jobs WHERE `company_id`='%s'"%(session['cid'])
		data['job']=select(q)
		if 'submit' in request.form:
			job=request.form['job']
			det=request.form['det']
			date=request.form['date']
			req=request.form['req']
			loc=request.form['loc']
			q="INSERT INTO `jobs` VALUES (null,'%s','%s','%s','%s','%s',curdate(),'pending')"%(session['cid'],job,req,det,date)
			insert(q)
			flash('JOB DETAILS ADDED')
			return redirect(url_for('company.company_Manage_job'))
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="DELETE FROM job WHERE job_id='%s'"%(id)
			delete(q)
			
			flash('JOB DETAILS DELETED')
			return redirect(url_for('company.company_Manage_job'))
		if action=='update':
			q="SELECT * FROM jobs WHERE job_id='%s'"%(id)
			data['job_up']=select(q)
		if 'updatez' in request.form:
			job=request.form['job']
			det=request.form['det']
			date=request.form['date']
			req=request.form['req']
			loc=request.form['loc']
			q="UPDATE `jobs` SET `job`='%s',`details`='%s',`last_date`='%s',qualification='%s',job_location='%s'  WHERE job_id='%s'"%(job,det,date,req,loc,id)
			
			update(q)
			flash('JOB DETAILS UPDATED')
			return redirect(url_for('company.company_Manage_job'))
		return render_template("company_Manage_job.html",data=data)
	else:
		return redirect(url_for('public.login'))