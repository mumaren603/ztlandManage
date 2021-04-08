from django.shortcuts import render,redirect,HttpResponse
from django.utils.decorators import method_decorator
from envManage import models
from django.views import View
from commonManage.views import envDetailInfoValidTemplate,addEnvValidTemplate,dbDetailInfoValidTemplate
import json
from commonManage import sqlQuery
from commonManage.views import getAuth,auth

#环境信息
@auth
def env(request):
    if request.method == 'GET':
        envInfo = models.EnvInfo.objects.all()
        # 获取权限
        auth = getAuth(request.session.get('username'))
        return render(request,'env.html',{'envinfo':envInfo,'auth':auth})
    else:
        return render(request, 'login.html')

# 环境详细信息
@auth
def envDetail(request, nid):
    if request.method == 'GET':
        # 获取权限
        auth = getAuth(request.session.get('username'))

        # 数据处理
        envNode = models.EnvInfo.objects.filter(m_id=nid).first()
        # 根据nid,查询出该环境前端、微服务、FTP
        frontService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid, service_model='前端')
        backService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid, service_model='后端')
        microService = models.EnvDetailInfo.objects.filter(env_sub_node=nid, service_model='微服务')
        FtpService = models.EnvDetailInfo.objects.filter(env_sub_node=nid, service_model='FTP')
        dbService = models.DbInfo.objects.filter(db_node_id=nid)
        # 返回信息有前端传过来入参nid? 主页面传过来参数便于子页面添加数据时和主页面数据关联
        return render(request, 'envDetail.html',
                      {'auth': auth, 'env_node_id': nid, 'envNode': envNode, 'frontService': frontService,
                       'backService': backService, 'microService': microService, 'FtpService': FtpService,
                       'dbService': dbService})
    else:
        return render(request, 'login.html')

# 环境详细信息编辑确定
class envDetailedit(View):
    def get(self,request):
        pass

    @method_decorator(auth)
    def post(self,request):
        res_msg = {'status': 0, 'err_msg': None}

        # id,service_url获取前端传来的，其余字段可以从obj获取.obj封装前端需要校验的字段
        id = request.POST.get('s_id')
        service_url = request.POST.get('service_url')
        service_deploy_path = request.POST.get('service_deploy_path')

        obj = envDetailInfoValidTemplate(request.POST)  # 将前端校验数据发给Front模板,Front模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                service_chinese_name = obj.cleaned_data.get('service_chinese_name')
                service_name = obj.cleaned_data.get('service_name')
                service_host = obj.cleaned_data.get('service_host')
                service_port = obj.cleaned_data.get('service_port')
                service_model = obj.cleaned_data.get('service_model')
                models.EnvDetailInfo.objects.filter(s_id=id).update(
                    service_chinese_name=service_chinese_name,
                    service_name=service_name,
                    service_host=service_host,
                    service_port=service_port,
                    service_model=service_model,
                    service_url=service_url,
                    service_deploy_path=service_deploy_path
                )
            except Exception as e:
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 数据库详细信息编辑确定
class dbDetailedit(View):
    def get(self,request):
        pass

    @method_decorator(auth)
    def post(self,request):
        res_msg = {'status': 0, 'err_msg': None}

        # obj封装前端需要校验的字段,以下字段为直接获取前端传过来的值，其他前端必填字段从校验模板对象获取即可
        db_id = request.POST.get('db_id')
        db_name = request.POST.get('db_name')

        obj = dbDetailInfoValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                db_ip = obj.cleaned_data.get('db_ip')
                db_port = obj.cleaned_data.get('db_port')
                db_sid = obj.cleaned_data.get('db_sid')
                db_user = obj.cleaned_data.get('db_user')
                db_password = obj.cleaned_data.get('db_password')
                models.DbInfo.objects.filter(db_id=db_id).update(
                    ip=db_ip,
                    port=db_port,
                    sid=db_sid,
                    user=db_user,
                    password=db_password,
                    name=db_name
                )
            except Exception as e:
                # print(e)                  #后期处理成记录到日志
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 删除操作
@auth
def envDel(request, nid):
    if request.method == 'GET':
        try:
            print('nid', nid)
            # 根据nid 查询所在行的env_sub_node_id ，方便删除完跳转到具体详情页面
            env_sub_node_id = models.EnvDetailInfo.objects.values('env_sub_node_id').filter(s_id=nid)
            print(env_sub_node_id)  # QuerySet
            env_sub_node_id = env_sub_node_id[0].get('env_sub_node_id')
            print("所属环境是：", env_sub_node_id)
            models.EnvDetailInfo.objects.filter(s_id=nid).delete()
        except Exception as e:
            print(e)
        return redirect('/envManage/env/detail-%s' % env_sub_node_id)


# 删除操作
@auth
def dbDel(request, nid):
    if request.method == 'GET':
        try:
            print('nid', nid)
            # 根据nid 查询所在行的env_sub_node_id ，方便删除完跳转到具体详情页面
            db_node_id = models.DbInfo.objects.values('db_node_id').filter(db_id=nid)
            db_node_id = db_node_id[0].get('db_node_id')
            models.DbInfo.objects.filter(db_id=nid).delete()
        except Exception as e:
            pass
            # print(e)  #后期写到日志
        return redirect('/envManage/env/detail-%s' % db_node_id)



# 查询(ajax，前端实现有问题)
# def envQuery(request):
#     if request.is_ajax():
#     # if request.method == 'POST':
#         res_msg={'code':0,'err_msg':None}
#
#         searchParam = request.POST.get('searchParam')
#         print('searchParam:%s' %searchParam)
#         try:
#             queryRes = models.EnvInfo.objects.filter(env_name=searchParam).first()
#             if queryRes:
#                 print('queryRes：',type(queryRes))
#                 # res_msg['data']=serializers.serialize('json',queryRes)
#                 return render(request, 'envQuery.html', {'queryRes': queryRes})
#                 print("11111")
#             else:
#                 res_msg['code']=1
#                 res_msg['err_msg']='查询结果不存在'
#         except:
#             res_msg['code']=1
#             res_msg['err_msg']="请求错误"
#         return HttpResponse(json.dumps(res_msg))

# 查询(非ajax)
@auth
def envQuery(request):
    if request.method == 'POST':
        queryParam = request.POST.get('searchParam')
        print('queryParam2',queryParam)
        if queryParam:
            try:
                # 环境信息支持模糊查询
                queryRes = models.EnvInfo.objects.filter(env_name__contains=queryParam).first()
                print(queryRes)
                return render(request, 'envQuery.html', {'queryRes': queryRes})
            except Exception as e:
                raise e
        else:
            return HttpResponse('请求错误')


# 添加环境主信息
@auth
def envAdd(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # status获取前端传来的，其余字段可以从obj获取.obj封装前端需要校验的字段
        status = request.POST.get('status')

        obj = addEnvValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                frontIP = obj.cleaned_data.get('frontIP')
                backIP = obj.cleaned_data.get('backIP')
                dbIP = obj.cleaned_data.get('dbIP')
                env_name = obj.cleaned_data.get('env_name')
                models.EnvInfo.objects.create(
                    frontIP=frontIP,
                    backIP=backIP,
                    dbIP=dbIP,
                    env_name=env_name,
                    status=status
                )
            except Exception as e:
                # print(e)                  #后期处理成记录到日志
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string


# 添加环境详细服务信息
@auth
def envDetailAdd(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # obj封装前端需要校验的字段,以下三个字段为直接获取前端传过来的值，其他前端必填字段从校验模板对象获取即可
        env_node_id = request.POST.get('env_node_id')
        service_url = request.POST.get('service_url')
        service_deploy_path = request.POST.get('service_deploy_path')

        obj = envDetailInfoValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
        print('obj,obj')
        v = obj.is_valid()
        if v:
            try:
                service_chinese_name = obj.cleaned_data.get('service_chinese_name')
                service_name = obj.cleaned_data.get('service_name')
                service_host = obj.cleaned_data.get('service_host')
                service_port = obj.cleaned_data.get('service_port')
                service_model = obj.cleaned_data.get('service_model')
                models.EnvDetailInfo.objects.create(
                    env_sub_node_id=env_node_id,
                    service_chinese_name=service_chinese_name,
                    service_name=service_name,
                    service_host=service_host,
                    service_port=service_port,
                    service_model=service_model,
                    service_url=service_url,
                    service_deploy_path=service_deploy_path
                )
            except Exception as e:
                # print(e)                  #后期处理成记录到日志
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string


# 添加数据库详细服务信息
@auth
def dbDetailAdd(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # obj封装前端需要校验的字段,以下三个字段为直接获取前端传过来的值，其他前端必填字段从校验模板对象获取即可
        env_node_id = request.POST.get('env_node_id')
        db_name = request.POST.get('db_name')

        obj = dbDetailInfoValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                db_ip = obj.cleaned_data.get('db_ip')
                db_port = obj.cleaned_data.get('db_port')
                db_sid = obj.cleaned_data.get('db_sid')
                db_user = obj.cleaned_data.get('db_user')
                db_password = obj.cleaned_data.get('db_password')
                models.DbInfo.objects.create(
                    db_node_id=env_node_id,
                    ip=db_ip,
                    port=db_port,
                    sid=db_sid,
                    user=db_user,
                    password=db_password,
                    name=db_name
                )
            except Exception as e:
                # print(e)                  #后期处理成记录到日志
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

