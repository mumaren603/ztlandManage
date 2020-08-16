from django.shortcuts import render,redirect,HttpResponse
from machine import models

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        UserQueryRes= models.UserInfo.objects.filter(username=uname,password=pwd).first()
        if UserQueryRes:
            request.session['username'] = uname
            request.session['is_login'] = True
            return redirect('/index')
        else:
            return render(request,'login.html')

def index(request):
    if request.session.get('is_login',None):
        return render(request,'index.html',{'user':request.session.get('username',None)})
    else:
        return HttpResponse('ERROR')

