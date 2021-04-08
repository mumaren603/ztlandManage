from django.shortcuts import render,redirect,HttpResponse
from commonManage import models
from django import forms
import json

# 登录
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}
        try:
            uname = request.POST.get('username')
            pwd = request.POST.get('password')
            UserQueryRes= models.UserInfo.objects.filter(username=uname,password=pwd).first()
            if UserQueryRes:
                request.session['username'] = uname
                request.session['is_login'] = True
                # 设置session过期时间为半小时
                request.session.set_expiry(60*30)
                #一周免登录
                if request.POST.get('login_remember') == '1':
                    request.session.set_expiry(60*60*24*7)
                res_msg['status'] = 0
                res_msg['err_msg'] = '登录成功'
            else:
                res_msg['status'] = 1
                res_msg['err_msg'] = '用户名或密码错误!'
        except Exception as e:
            res_msg['status'] = 1
            res_msg['err_msg'] = e
    return HttpResponse(json.dumps(res_msg))  # string

# 登出
def logout(request):
    if request.method == "GET":
        request.session.clear()
        return redirect('/common/login')


#装饰器 判断session会话是否过期,后续所有请求需要调用该装饰器
def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get('is_login'):
            return render(request, 'login.html')
        ret = func(request,*args,**kwargs)
        return ret
    return inner

#获取权限
def getAuth(username):
    res = models.UserInfo.objects.filter(username=username)
    user_auth=[]
    for row in res:
        print('用户名',row.username)
        for v in row.auth_rel.all():
            user_auth.append(v.authcode)
        print('用户权限', user_auth)
        return user_auth

#主页
def index(request):
    if request.session.get('is_login',None):
        return render(request,'index.html',{'user':request.session.get('username',None)})
    else:
        return render(request,'login.html')


'''校验模板，如环境详细信息校验模板，数据库校验模板'''
# 定义校验模板 -->环境详情界面编辑弹出框/添加弹出框提交时字段校验.
class envDetailInfoValidTemplate(forms.Form):
    service_chinese_name = forms.CharField(error_messages={'required': '服务名不可为空！'})
    service_name = forms.CharField(error_messages={'required': '服务标识不可为空！'})
    service_host = forms.GenericIPAddressField(error_messages={'required': 'IP地址不可为空！', 'invalid': 'IP地址格式错误！'})
    service_port = forms.IntegerField(max_value=65535,
                                      min_value=1,
                                      error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                      )
    service_model = forms.CharField(error_messages={'required': '所属节点不可为空！'})

# 定义添加主环境信息模板校验
class addEnvValidTemplate(forms.Form):
    frontIP = forms.GenericIPAddressField(error_messages={'required': '前端IP地址不可为空！', 'invalid': '前端IP地址格式错误！'})
    backIP = forms.GenericIPAddressField(error_messages={'required': '后端IP地址不可为空！', 'invalid': '后端IP地址格式错误！'})
    dbIP = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    env_name = forms.CharField(error_messages={'required': '所属环境不可为空！'})

# 定义校验模板 -->数据库详情界面编辑弹出框/添加弹出框提交时字段校验.
class dbDetailInfoValidTemplate(forms.Form):
    db_ip = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    db_port = forms.IntegerField(max_value=65535,
                                 min_value=1,
                                 error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                )
    db_sid = forms.CharField(error_messages={'required': '数据库实例不可为空！'})
    db_user = forms.CharField(error_messages={'required': '数据库用户名不可为空！'})
    db_password = forms.CharField(error_messages={'required': '数据库密码不可为空！'})


'''数据库通用操作，包括数据库连接，释放，查询等'''
import cx_Oracle as Oracle

class DBAction():
    def __init__(self ,connInfo):
        self.conn = Oracle.Connection(connInfo)
        print("数据库连接信息是：",self.conn)

    def SqlExecute(self,sql):
        cursor = self.conn.cursor()
        try:
            res = cursor.execute(sql)
            print("执行的sql：%s" %res)
            queryResult = res.fetchone()    # 元祖
            # queryResult = queryResult[0]  # 取元祖第一个值
            return queryResult
        except Exception as e:
            raise
            print('异常',e)
        finally:
            cursor.close()

    def closeConn(self):
        self.conn.close()

if __name__ =='__main__':
    pass
    # connInfo = 'DJJGK/DJJGK@172.0.0.250/orcldj'
    # DBAction(connInfo).getQueryRes()