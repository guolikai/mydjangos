from django.shortcuts import render,redirect
from ucenter import models
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def register(request,*args,**kwargs):
    ret = {'status':''}
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        username = request.POST.get('username',None)
        mobile = request.POST.get('mobile',None)
        department = request.POST.get('department',None)
        remark = request.POST.get('remark',None)
        print(email,password,username)
        is_empty = all([email,password,username])
        if is_empty:
            count = models.UserProfile.objects.filter(email=email).count()
            if count == 0:
                encrypt_password = make_password(password)
                models.UserProfile.objects.create(email=email,password=encrypt_password,name=username,
                                                  mobile=mobile,department=department,remark =remark)
                ret['status']="注册成功"
                return redirect("/app01/login")
            else:
                ret['status'] = "用户%s已存在" % email
                return redirect("/app01/login")
        else:
            ret['status'] = "Email、Password、Username三项不能为空"
    return render(request,'ucenter/register.html',ret)

def forgetpass(request,*args,**kwargs):
    ret = {'status':''}
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        password2 = request.POST.get('password2',None)
        is_empty = all([email,password,password2])
        if is_empty:
            if password == password2:
                encrypt_password = make_password(password)
                count = models.UserProfile.objects.filter(email=email).count()
                if count != 0:
                    models.UserProfile.objects.filter(email=email).update(password=encrypt_password)
                    ret['status']="用户密码修改成功"
                    return redirect("/app01/login")
                else:
                    ret['status']="用户%s不存在" % email
            else:
                ret['status'] = "2次输入密码不一样"
        else:
            ret['status'] = "用户信息及密码不能为空"
    return render(request,'ucenter/forgetpass.html',ret)