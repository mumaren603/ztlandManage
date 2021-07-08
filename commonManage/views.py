from django.shortcuts import render,redirect,HttpResponse
from commonManage import models
from django import forms
from commonManage.logFunc import loggerConf

logger = loggerConf().getLogger()

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
        res = func(request,*args,**kwargs)
        return res
    return inner

#获取权限
def getAuth(username):
    res = models.UserInfo.objects.filter(username=username)
    user_auth=[]
    for row in res:
        logger.debug('用户名:%s' % row.username)
        for v in row.auth_rel.all():
            user_auth.append(v.authcode)
        logger.debug('用户权限:%s'  % user_auth)
        return user_auth

#主页
def index(request):
    if request.session.get('is_login',None):
        return render(request,'index.html',{'user':request.session.get('username',None)})
    else:
        return render(request,'login.html')


'''校验模板，如环境详细信息校验模板，数据库校验模板'''
# 环境管理模块-->环境详情界面编辑弹出框/添加弹出框字段校验.
class envDetailInfoValidTemplate(forms.Form):
    service_chinese_name = forms.CharField(error_messages={'required': '服务名不可为空！'})
    service_name = forms.CharField(error_messages={'required': '服务标识不可为空！'})
    service_host = forms.GenericIPAddressField(error_messages={'required': 'IP地址不可为空！', 'invalid': 'IP地址格式错误！'})
    service_port = forms.IntegerField(max_value=65535,
                                      min_value=1,
                                      error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                      )
    service_model = forms.CharField(error_messages={'required': '所属节点不可为空！'})

# 环境管理模块--> 环境主界面编辑弹出框/添加弹出框字段校验.
class envValidTemplate(forms.Form):
    frontIP = forms.GenericIPAddressField(error_messages={'required': '前端IP地址不可为空！', 'invalid': '前端IP地址格式错误！'})
    backIP = forms.GenericIPAddressField(error_messages={'required': '后端IP地址不可为空！', 'invalid': '后端IP地址格式错误！'})
    dbIP = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    env_name = forms.CharField(error_messages={'required': '所属环境不可为空！'})

# 环境管理模块--> 数据库详情界面编辑弹出框/添加弹出框字段校验.
class dbDetailInfoValidTemplate(forms.Form):
    db_ip = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    db_port = forms.IntegerField(max_value=65535,
                                 min_value=1,
                                 error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                )
    db_sid = forms.CharField(error_messages={'required': '数据库实例不可为空！'})
    db_user = forms.CharField(error_messages={'required': '数据库用户名不可为空！'})
    db_password = forms.CharField(error_messages={'required': '数据库密码不可为空！'})

# 主机管理模块-->主机信息编辑弹出框/添加弹出框字段校验.
class hostInfoValidTemplate(forms.Form):
    intranetIP = forms.GenericIPAddressField(error_messages={'required': '内网IP地址不可为空！', 'invalid': '内网IP地址格式错误！'})
    serverType = forms.CharField(error_messages={'required': '机器类型不可为空！'})
    serverOs = forms.CharField(error_messages={'required': '操作系统不可为空！'})
    serverAccount = forms.CharField(error_messages={'required': '用户名不可为空！'})
    serverPassword = forms.CharField(error_messages={'required': '密码不可为空！'})


'''数据库通用操作，包括数据库连接，释放，查询等'''
import cx_Oracle as Oracle

class DBAction():
    def __init__(self ,connInfo):
        self.conn = Oracle.Connection(connInfo)
        self.cursor = self.conn.cursor()

    def SqlExecute(self,sql):
        try:
            res = self.cursor.execute(sql)
            logger.debug("执行的sql：%s" % sql)
            queryResult = res.fetchone()    # 元祖
            return queryResult
        except Exception as e:
            raise
            logger.error("异常信息：%s" % e)

    def closeConn(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# 分页
# data_count=[]                                      # 数据总条数
# for i in range(1090):
#     data_count.append(i)
# def page_list(request):
#     current_page =  request.GET.get('page',1)      # 当前页  如果不存在默认展示第一页
#     current_page = int(current_page)
#
#     per_page_count=10                              # 每页显示10条
#     start_v = (current_page-1)*per_page_count      # 页面数据起始
#     end_v = (current_page)*per_page_count          # 页面数据结束
#
#     # data = data_count[0:10]
#     data = data_count[start_v:end_v]               # 当前页面战术数据范围 如【10,20】
#
#     all_count = len(data_count)                    # 数据总条数
#     totalCount ,y = divmod(all_count,per_page_count)     #根据每页展示数据条数（如一页展示10条）获取整个数据会有多少个页码
#     if y:
#         totalCount += 1        #y不为0，那总得页数就的+1，y为0  那总页数就等于totalcount
#
#     page_list= []
#     pager_num =11              #以下逻辑处理页码极端值处理，页码最前面，最后面等页码处理　
#     if totalCount < pager_num:                     # 如果总页数小于11，那么页数范围就是【1，总页数】
#         start_index = 1
#         end_index = totalCount+1                   # 当前页取不到，所以要加1
#     else:
#         if current_page <= (pager_num+1)/2:        # 总页数大于11，当前页码小于等于6，那么页数范围就是【1,11】
#             start_index = 1
#             end_index = pager_num+1
#         else:
#             start_index = current_page - (pager_num-1)/2
#             end_index = current_page + (pager_num+1)/2
#             if (current_page +(pager_num-1)/2) > totalCount:   # 处理最后页码问题
#                 start_index = totalCount-pager_num +1
#                 end_index = totalCount + 1
#
#     if current_page == 1:
#         prev = '<a class="page" href="javascript:void(0)">上一页</a>'   #javascript:void(0);  代表什么都不做
#     else:
#         prev = '<a class="page" href="/common/page_list?page=%s">上一页</a>' % (current_page-1)
#     page_list.append(prev)
#
#     for i in range(int(start_index),int(end_index)):
#         if i == current_page:
#             temp = '<a class="page active" href="/common/page_list?page=%s">%s</a>' % (i, i)
#         else:
#             temp = '<a class="page" href="/common/page_list?page=%s">%s</a>' %(i,i)
#         page_list.append(temp)
#
#     if current_page == totalCount:
#         next = '<a class="page" href="javascript:void(0)">下一页</a>'
#     else:
#         next = '<a class="page" href="/common/page_list?page=%s">下一页</a>' % (current_page + 1)
#     page_list.append(next)
#
#     jump = '''
#     <input type="text"/><a onclick="jumpTo(this,'/common/page_list?page=')" id="ii1">跳转</a>
#     <script>
#     function jumpTo(ths,base){
#         val = ths.previousSibling.value;
#         location.href = base + val;
#     }
#     </script>
#     '''
#     page_list.append(jump)
#
#     page_str="".join(page_list)          #将列表转化为字符串
#     from django.utils.safestring import mark_safe
#     page_str = mark_safe(page_str)       #防止XSS攻击 比如评论区写上一些代码，浏览器不会解析而是把当前脚本当成字符串处理返回
#
#     return render(request,"page.html",{'data':data,'page_str':page_str})


# 分页封装实现
from django.utils.safestring import mark_safe

class Page:
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property    #装饰器@property ，后面引用地方就不用加括号。
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        page_list = []

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page == 1:
            prev = '<div class="page"><a href="javascript:void(0);">上一页</a></div>'
        else:
            prev = '<div class="page"><a href="%s?p=%s">上一页</a></div>' % (base_url, self.current_page - 1,)
        page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<div class="page_num page_active"><a href="%s?p=%s">%s</a></div>' % (base_url, i, i)
            else:
                temp = '<div class="page_num"><a href="%s?p=%s">%s</a></div>' % (base_url, i, i)
            page_list.append(temp)

        if self.current_page == self.total_count:
            next = '<div class="page"><a href="javascript:void(0);">下一页</a></div>'
        else:
            next = '<div class="page"><a href="%s?p=%s">下一页</a></div>' % (base_url, self.current_page + 1,)

        page_list.append(next)

        jump = """
        <input style="width:120px;" type='text'/><a onclick='jumpTo(this, "%s?p=");'>GO</a>
        <script>
            function jumpTo(ths,base){
                var val = ths.previousSibling.value;
                location.href = base + val;
            }
        </script>
        """ % (base_url,)

        page_list.append(jump)

        page_str = mark_safe("".join(page_list))

        return page_str






















