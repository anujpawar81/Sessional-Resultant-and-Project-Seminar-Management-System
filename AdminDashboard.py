from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from datetime import date
import json
import requests
import pandas as pd
import urllib.request
from datetime import datetime
from urllib.request import Request, urlopen
from django.core.files.storage import FileSystemStorage
import requests
mydb=pymysql.connect(host="localhost",user="root",password="root",database="eventconduct")
def index(request):
    return render(request,"index.html")


