from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
import pymysql
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
import random

mydb=pymysql.connect(host="localhost",user="root",password="root",database="sessional")

def studentlogin(request):
    

    return render(request,"StudentLogin.html")


def contact(request):
    

    return render(request,"StudentLogin.html")

def facultylogin1(request):

    return render(request,"FacultyLogin.html")



def adminlogin(request):

    return render(request,"AdminLogin.html")



def ViewMarkStudents(request):
    content={}
    payload=[]
    payload2=[]
    total=0;
    q1="select * from testresult where studid=%s";
    uid=request.session['uid']
    print(uid)
    values=(uid)
    cur=mydb.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        total=total+int(x[6])
        mark1=int(x[6])
        if(mark1>=12):
            content={'result':'Pass','tid':x[0],'name':x[2],'Branch':x[4],'Year':x[5],'Marks':x[6],'Subject':x[8]}
        else:
             content={'result':'Fail','tid':x[0],'name':x[2],'Branch':x[4],'Year':x[5],'Marks':x[6],'Subject':x[8]}
            
        payload.append(content)
        content={}
    print(payload)
    
    per=total/120;
    per=per*100;
    
    content1={'total':total,'per':per}
    payload2.append(content1)
    
    return render(request,"ViewMarkStudents.html",{'list': {'items':payload},'list1': {'items1':payload2}})



def StudLogin(request):
    email=request.POST.get("email")
    #passw=request.POST.get("pass")
    print("email",email)
    #print(passw)
    content={}
    payload=[]
    q1="select * from users";
    
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    count=0
    for x in res:
        
        if(x[6]=="Student"):
            #print(x[2])
            print(x[3])
            if(x[2].strip()==email.strip()):
                print(x)
                content={'allotime':x[9],'semdate':x[8],'group':x[12],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
                request.session['uid']=x[2]
                request.session['name']=x[0]
                payload.append(content)
                content={}
                count=1
    if(count==1):
        return render(request,"StudentDashboard.html",{'list': {'items':payload}})
    else:
        return render(request,"HomePage.html",{'list': {'items':payload}})




def creategroup2(request):
    uid=request.GET.get("uid")
    request.session['uid']=uid

    return render(request,"CreateGroup2.html")



def creategroup3(request):
    uid=request.session['uid']
    print("uid",uid)
    group=request.POST.get("group")
    query="update users set sgroup=%s where uid=%s"
    values=(group,uid)
    c1=mydb.cursor()
    c1.execute(query,values)
    mydb.commit()
    return render(request,"CreateGroup1.html")

def creategroup1(request):
    branch=request.POST.get("branch")
    year=request.POST.get("year")
    content={}
    payload=[]
    q1="select * from users where Branch=%s and Year=%s";
    values=(branch,year)
    cur=mydb.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            content={'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"CreateGroup1.html",{'list': {'items':payload}})


def AdmLogin(request):
    email=request.POST.get("email")
    passw=request.POST.get("pass")
    if(email=="admin" and passw=="admin"):
        content={}
        payload=[]
        q1="select * from users";
        cur=mydb.cursor()
        cur.execute(q1)
        res=cur.fetchall()
        for x in res:
            if(x[6]=="Student"):
                content={'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
                payload.append(content)
                content={}      
        return render(request,"AdminDashboard.html",{'list': {'items':payload}})
    else:
        return render(request,"HomePage.html")

def schedulesem(request):
    
    branch=request.POST.get("branch")
    year=request.POST.get("year")
    numberstud=request.POST.get("numberstud")
    starttime=request.POST.get("starttime")
    date=request.POST.get("date")
    print("start time",starttime)
    str11=starttime.split(":")
    hrs=int(str11[0])
    minute=int(str11[1])
    print("Hrs",hrs)
    print("minute",minute)
    content={}
    payload=[]
    studcount=0;
    allottime="";
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            if(x[4]==branch and x[5]==year and x[10]=='0' ):
                studcount=studcount+1
                if(studcount<int(numberstud)):
                    if(minute>60):
                        minute=0
                        hrs=hrs+1
                    allottime=""+str(hrs)+" : "+str(minute)
                    print("time",str(allottime))
                    content={'semdate':date,'allotime':allottime, 'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
                    print(content)  
                    payload.append(content)
                    content={}
                    sql="update users set semdate=%s,semtime=%s,isdone=%s where uid=%s"
                    values=(date,allottime,'0',x[7])
                    c1=mydb.cursor()
                    c1.execute(sql,values)
                    mydb.commit()
                    minute=minute+10
                    
                
    return render(request,"ScheduleSeminar1.html",{'list': {'items':payload}})

def markasdone(request):
    studid=request.session['uid']
    remark=request.POST.get("remark")
    qe="update users set remark=%s,isdone=%s where uid=%s"
    values=(remark,'1',studid)
    c1=mydb.cursor()
    c1.execute(qe,values)
    mydb.commit()
    today = date.today()
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            content={'group':x[12],'semdate':x[8],'allotime':x[9],'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"FacultyDashboard.html",{'list': {'items':payload}})

def schedulesem1(request):
    return render(request,"ScheduleSeminar.html")
def reschedule1(request):
    studid=request.session['uid']
    date1=request.POST.get("date")
    time1=request.POST.get("date")
    qe="update users set semdate=%s,semtime=%s where uid=%s"
    values=(date1,time1,studid)
    c1=mydb.cursor()
    c1.execute(qe,values)
    mydb.commit()
    today = date.today()
    content={}
    payload=[]
    q1="select * from users where isdone='0'";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student" and x[8]==""+str(today)):
            content={'semdate':x[8],'allotime':x[9],'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"FacultyDashboard.html",{'list': {'items':payload}})
def reschedule(request):
    studid=request.GET.get("uid")
    request.session['uid']=studid
    return render(request,"Reschedule.html")
def remark(request):
    studid=request.GET.get("uid")
    request.session['uid']=studid
    return render(request,"Remark.html")

def About(request):
    return render(request,"About.html")
def Home(request):
    return render(request,"HomePage.html")
def inde(request):
    return render(request,"signin.html")

def Logout(request):
    return render(request,"HomePage.html")

def admindashboard(request):
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            content={'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}      
    return render(request,"AdminDashboard.html",{'list': {'items':payload}})

def facdashboard(request):
    today = date.today()
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student" ):
            content={'group':x[12],'semdate':x[8],'allotime':x[9],'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"FacultyDashboard.html",{'list': {'items':payload}})
    

def AddFaculty(request):
    return render(request,"AddFaculty.html")
def ViewTestResult(request):
    content={}
    payload=[]
    q1="select * from test";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'tid':x[0],'name':x[1]}
        payload.append(content)
        content={}
    print(payload)
    return render(request,"ViewTestResult.html",{'list': {'items':payload}})

def ViewTestResult1(request):
    test=request.POST.get("test")
    content={}
    payload=[]
    q1="select * from testresult where subject=%s";
    values=(test)
    cur=mydb.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        content={'tid':x[0],'name':x[2],'Branch':x[4],'Year':x[5],'Marks':x[6]}
        payload.append(content)
        content={}
    print(payload)
    return render(request,"ViewTestResult1.html",{'list': {'items':payload}})
def AddFaculty1(request):
    name=request.POST.get("name")
    cnum=request.POST.get("cnumber")
    email=request.POST.get("email")
    passw=request.POST.get("pass")
    role="Faculty"
    sql="INSERT INTO users(Name,Cnum,Email,Passw,urole)VALUES (%s,%s,%s,%s,%s)";
    values=(name,cnum,email,passw,role)
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"AddFaculty.html")

def AddStudent(request):
    return render(request,"AddStudent.html")

def CreateTest(request):
    return render(request,"CreateTest.html")
    

def CreateTest1(request):
    uid=request.session['uid']
    name=request.POST.get("name")
    tdate=request.POST.get("date")
    tmark=request.POST.get("tmark")
    byfac=request.session['name']
    sql="INSERT INTO test(TestName,TDate,Marks,byfac,fid)VALUES (%s,%s,%s,%s,%s)";
    values=(name,tdate,tmark,byfac,uid)
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"CreateTest.html")


def AddStudent1(request):
    name=request.POST.get("name")
    cnum=request.POST.get("cnumber")
    email=request.POST.get("email")
    passw=request.POST.get("pass")
    branch=request.POST.get("branch")
    year=request.POST.get("year")
    role="Student"
    sql="INSERT INTO users(Name,Cnum,Email,Passw,urole,Branch,Year)VALUES (%s,%s,%s,%s,%s,%s,%s)";
    values=(name,cnum,email,passw,role,branch,year)
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"AddStudent.html")
def UploadMark2(request):
    uid11=request.GET.get("uid")
    content={}
    payload=[]
    request.session['studid']=uid11
    q1="select * from test";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'tid':x[0],'name':x[1]}
        payload.append(content)
        content={}
    print(payload)
    return render(request,"UploadMark2.html",{'list': {'items':payload}})

def UploadMark3(request):
    test=request.POST.get("test")
    marksobt=request.POST.get("marks")
    studid=request.session['studid']
    print("studid",studid)
    
    q1="select * from users where uid=%s";
    cur=mydb.cursor()
    value=(studid)
    cur.execute(q1,value)
    res=cur.fetchall()
    name=""
    cnum=""
    branch=""
    year=""
    for x in res:
        print("x[7]",x[7])
        name=x[0]
        cnum=x[1]
        branch=x[4]
        year=x[5]
            
    sql="INSERT INTO testresult(testid,StudName,Cnum,Branch,Year,markobtain,studid)VALUES (%s,%s,%s,%s,%s,%s,%s)";
    values=(test,name,cnum,branch,year,marksobt,studid)
    cur=mydb.cursor()
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"UploadMark1.html")

def UploadMark1(request):
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            content={'uid':x[7],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"UploadMark1.html",{'list': {'items':payload}})
def ViewStudent(request):
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Student"):
            content={'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"ViewStudent.html",{'list': {'items':payload}})
def FacLogin(request):
    email=request.POST.get("email")
    passw=request.POST.get("pass")
    print(email)
    print(passw)
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    count=0
    for x in res:
        if(x[6]=="Faculty"):
            content={'remark':x[11],'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            request.session['uid']=x[7]
            request.session['name']=x[0]
            payload.append(content)
            content={}
            count=1
    if(count==1):
        return render(request,"FacultyDashboard.html",{'list': {'items':payload}})
    else:
        return render(request,"HomePage.html",{'list': {'items':payload}})

def ViewFaculty(request):
    content={}
    payload=[]
    q1="select * from users";
    cur=mydb.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        if(x[6]=="Faculty"):
            content={'name':x[0],"email":x[2],"cnum":x[1],"branch":x[4],"year":x[5]}
            payload.append(content)
            content={}
    return render(request,"ViewFaculty.html",{'list': {'items':payload}})

def service(request):
    return render(request,"service.html")

def admindashboard(request):
     return render(request,"admindashboard.html")
def nanalyze(request):
     return render(request,"nanalyze.html")

def removeproduct(request):
    content={}
    payload=[]
    q1="select * from userdata";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'name':x[0],'contact':x[1],"email":x[2]}
        payload.append(content)
        content={}
    return render(request,"removeuserprofile.html",{'list': {'items':payload}})

def doremoveproduct(request):
    name=request.GET.get('email')
    q1="delete from userdata where email=%s";
    values=(name)
    cur=con.cursor()
    cur.execute(q1,values)
    con.commit()
    removeproduct(request)
    return render(request,"removeuserprofile.html")


def dashremove(request):
    return render(request,"removeuserprofile.html")

def viewpredicadmin(request):
    content={}
    payload=[]
    q1="select * from smp";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'s1':x[0],"s2":x[1],"s3":x[2],"s4":x[3],'s5':x[4],"s6":x[5],"s7":x[6],"s8":x[7],"pred":x[8],"acc":x[9]}
        payload.append(content)
        content={}
    return render(request,"viewpredadmin.html",{'list': {'items':payload}})
    

def dataset(request):
    return render(request,"adminhospital.html")

def hospitalregister(request):
    hospital_name=request.POST.get('hospital_name')
    city=request.POST.get('city')
    address=request.POST.get('address')
    sql="INSERT INTO hospital(hospital_name,city,address) VALUES (%s,%s,%s)";
    values=(hospital_name,city,address)
    cur=con.cursor()
    cur.execute(sql,values)
    con.commit()
    message = "You are successfully registered"
    return render(request,"adminhospital.html",{'message':message})

def findhospital(request):
    return render(request,"findhospital.html")

def showhospital(request):
    city=request.POST.get('city')
    address=request.POST.get('address')
    content={}
    payload=[]
    sql="SELECT * FROM hospital WHERE address=%s OR city=%s";
    values=(city,address)
    cur=con.cursor()
    cur.execute(sql,values)
    res=cur.fetchall()
    for x in res:
        content={'hospital_name':x[1],"City":x[2]}
        payload.append(content)
        content={}
    return render(request,"analyze.html",{'payload': payload})




def prevpred(request):
    content={}
    payload=[]
    uid=request.session['uid']
    q1="select * from smp where uid=%s";
    values=(uid)
    cur=con.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        content={'s1':x[0],"s2":x[1],"s3":x[2],"s4":x[3],'s5':x[4],"s6":x[5],"s7":x[6],"s8":x[7],"pred":x[8],"acc":x[9]}
        payload.append(content)
        content={}
    return render(request,"prevpred.html",{'list': {'items':payload}})

def myprofile(request):
    content={}
    payload=[]
    uid=request.session['uid']
    q1="select * from userdata where uid=%s";
    values=(uid)
    cur=con.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        content={'name':x[0],"contact":x[1],"email":x[2]}
        payload.append(content)
        content={}
    return render(request,"myprofile.html",{'list': {'items':payload}})


def viewuser(request):
    content={}
    payload=[]
    q1="select * from userdata";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'name':x[0],"contact":x[1],"email":x[2]}
        payload.append(content)
        content={}
    return render(request,"viewuserprofile.html",{'list': {'items':payload}})



def dologin(request):
    sql="select * from userdata";
    cur=con.cursor()
    cur.execute(sql)
    data=cur.fetchall()
    email=request.POST.get('emai')
    password=request.POST.get('passw')
    name="";    
    uid="";
    isfound="0";
    content={}
    payload=[]
    print(email)
    print(password)
    if(email=="admin" and password=="admin"):
        print("print")
        return render(request,"admindashboard.html")
    else:
        for x in data:
            if(x[2]==email and x[3]==password):
                request.session['uid']=x[4]
                request.session['name']=x[0]
                request.session['contact']=x[1]
                request.session['email']=x[2]
                request.session['pass']=x[3]
                isfound="1"
        if(isfound=="1"):
             return render(request,"index.html")
        else:
             return render(request,"error.html")
       
    
def login(request):
    return render(request,"loginpanel.html")
    
def logout(request):
    return render(request,"loginpanel.html")

def register(request):
    return render(request,"registrationPanel.html")
def livepred(request):
    return render(request,"predict.html")


def dashboard(request):
    return render(request,"admindashboard.html")

def doregister(request):
    name=request.POST.get('uname')
    cnumber=request.POST.get('cno')
    email=request.POST.get('email')
    password=request.POST.get('passw')
    sql="INSERT INTO userdata(name,contact,email,password) VALUES (%s,%s,%s,%s)";
    values=(name,cnumber,email,password)
    cur=con.cursor()
    cur.execute(sql,values)
    con.commit()
    return render(request,"loginpanel.html")



