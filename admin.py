from flask import *
from database import *
admin=Blueprint("admin",__name__)


@admin.route('/adminhome')
def adminhome():
    return render_template("adminhome.html")

 
@admin.route('/admin_view_company',methods=['get','post'])
def viewcompany():
    data={}
    s="select * from company inner join login using(login_id)"
    se=select(s)
    print(se)
    data['key']=se
    # if 'action' in request.args:
    #     print("1111111111111111")
    #     action=request.args["action"]
    #     id=request.args["id"]
    # if action == "approve":
    #     print("222222222222222222")
    #     u ="update login set usertype=='company' where login_id='%s'"%(id)
    #     update(u)
   
    return render_template('admin_view_company.html',data=data)



@admin.route('/admin_approve_company',methods=['get','post'])
def admin_approve_company():
    id=request.args['id']
    u ="update login set usertype='company' where login_id='%s'"%(id)
    update(u)

    return redirect(url_for('admin.viewcompany'))
    


@admin.route('/admin_view_job',methods=['get','post'])
def admin_view_job():
    id=request.args['id']
    data={}
    s="select * from company where login_id='%s'"%(id)
    se=select(s)
    cid=se[0]['company_id']
    j="select * from jobs where company_id='%s'"%(cid)
    jo=select(j)
    data['key']=jo
   
    return render_template('admin_view_job.html',data=data)

@admin.route("/experience_type",methods=['get','post'])
def experience_type():
    
    data={}
    se="select * from experience_type" 
    print(se)
    s=select(se)
    data['key']=s

    if 'submit' in request.form:
        experience_type=request.form['experience_type']
        year=request.form['year']

        a="insert into experience_type values(null,'%s','%s')"%(experience_type,year)
        insert(a)
        return redirect(url_for('admin.experience_type'))
    return render_template("experience_type.html",data=data)

@admin.route('/view_feedback',methods=['get','post'])
def view_feedback():
    
    data={}
    s="select * from feedback " 
    se=select(s)
    print(se)
    data['key']=se

    return render_template('view_feedback.html',data=data)

@admin.route('/add_aptitude_test',methods=['get','post'])
def aptitude_test():
    data={}
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
        
        q="insert into apti_test values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(experience_type,job_role,ques,opt1,opt2,opt3,opt4,crt_opt)
        id=insert(q)

    return render_template('add_aptitude_test.html',data=data)

@admin.route("/job_role",methods=['get','post'])
def job_role():
    
    data={}
    se="select * from job_role" 
    print(se)
    s=select(se)
    data['key']=s

    if 'submit' in request.form:
        job_role=request.form['job_role']

        a="insert into job_role values(null,'%s')"%(job_role)
        insert(a)
        return redirect(url_for('admin.adminhome'))
    return render_template("job_role.html",data=data)


@admin.route("/admin_view_application",methods=['get','post'])
def admin_view_application():
    
    data={}
    se="select * from application_request inner join jobs using(job_id) inner join user using(user_id) inner join company using(company_id)"
    print(se)
    s=select(se)
    data['key']=s
    return render_template('admin_view_application.html',data=data)

@admin.route('/admin_view_participants')
def admin_view_participants():
    data={}
    s="select * from apti_answers inner join user using(user_id) "
    data['key']=select(s)
    return render_template('admin_view_participants.html',data=data)
