"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index
##from . import UserDashboard
##from . import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('facultylogin1', index.facultylogin1),
    path('ViewMarkStudents', index.ViewMarkStudents),
    path('About', index.About),
    path('StudLogin1', index.studentlogin),
    path('StudLogin1', index.studentlogin),
    path('AdminLogin', index.adminlogin),
    path('StudLogin', index.StudLogin),
    path('creategroup3', index.creategroup3),
    path('creategroup2', index.creategroup2),
    path('creategroup1', index.creategroup1),
    path('AdmLogin', index.AdmLogin),
    path('reschedule1', index.reschedule1),
    path('reschedule', index.reschedule),
    path('remark', index.remark),
    path('markasdone', index.markasdone),
    path('schedulesem', index.schedulesem),
    path('schedulesem1', index.schedulesem1),
    path('creategroup1', index.creategroup1),
    path('admindashboard', index.admindashboard),
    path('facdashboard', index.facdashboard),
    path('index', index.inde),
    path(' ', index.Home),
    path('Home', index.Home),
    path('AddFaculty', index.AddFaculty),
    path('AddFaculty1', index.AddFaculty1),
    path('AddStudent', index.AddStudent),
    path('AddStudent1', index.AddStudent1), 
    path('ViewStudent', index.ViewStudent),
    path('ViewFaculty', index.ViewFaculty),
    path('FacLogin', index.FacLogin),
    path('CreateTest', index.CreateTest),
    path('CreateTest1', index.CreateTest1),
    path('UploadMark1', index.UploadMark1),
    path('UploadMark2', index.UploadMark2),
    path('UploadMark3', index.UploadMark3),
    path('ViewTestResult', index.ViewTestResult),
    path('ViewTestResult1', index.ViewTestResult1),
    path('Logout', index.Logout)
      
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

