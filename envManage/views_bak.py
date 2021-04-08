from django.shortcuts import render,redirect,HttpResponse
from envManage import models
from django.views import View
from commonManage.views import envDetailInfoValidTemplate,addEnvValidTemplate,dbDetailInfoValidTemplate
import json
from commonManage import sqlQuery
from commonManage.views import getAuth

# 环境信息
def env(request):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            envInfo = models.EnvInfo.objects.all()
            # 获取权限
            auth = getAuth(request.session.get('username'))
            return render(request,'env.html',{'envinfo':envInfo,'auth':auth})
    else:
        return render(request, 'login.html')


# 环境详细信息
def envDetail(request,nid):
    if request.session.get('is_login', None):
        if request.method == 'GET':
            # 获取权限
            auth = getAuth(request.session.get('username'))

            #数据处理
            envNode = models.EnvInfo.objects.filter(m_id=nid).first()
            # 根据nid,查询出该环境前端、微服务、FTP
            frontService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid,service_model = '前端')
            backService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid,service_model = '后端')
            microService = models.EnvDetailInfo.objects.filter(env_sub_node=nid,service_model= '微服务')
            FtpService = models.EnvDetailInfo.objects.filter(env_sub_node=nid,service_model= 'FTP')
            dbService = models.DbInfo.objects.filter(db_node_id=nid)
            # 返回信息有前端传过来入参nid? 主页面传过来参数便于子页面添加数据时和主页面数据关联
            return render(request, 'envDetail.html', {'auth':auth,'env_node_id':nid, 'envNode':envNode, 'frontService':frontService, 'backService':backService, 'microService':microService, 'FtpService':FtpService, 'dbService':dbService})
    else:
        return render(request, 'login.html')

# 环境详细信息编辑确定
class envDetailedit(View):
    def get(self,request):
        pass

    def post(self, request):
        if request.session.get('is_login', None):
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
        else:
            return render(request, 'login.html')

# 数据库详细信息编辑确定
class dbDetailedit(View):
    def get(self,request):
        pass

    def post(self,request):
        if request.session.get('is_login', None):
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
        else:
            return render(request, 'login.html')

# 环境信息删除操作
def envDel(request,nid):
    if request.session.get('is_login',None):
        if request.method == 'GET':
            try:
                print('nid',nid)
                # 根据nid 查询所在行的env_sub_node_id ，方便删除完跳转到具体详情页面
                env_sub_node_id = models.EnvDetailInfo.objects.values('env_sub_node_id').filter(s_id=nid)
                print(env_sub_node_id) #QuerySet
                env_sub_node_id = env_sub_node_id[0].get('env_sub_node_id')
                print("所属环境是：",env_sub_node_id)
                models.EnvDetailInfo.objects.filter(s_id=nid).delete()
            except Exception as e:
                    print(e)
            return redirect('/envManage/env/detail-%s' %env_sub_node_id)
    else:
        return render(request,'login.html')

# 数据库删除操作
def dbDel(request,nid):
    if request.session.get('is_login',None):
        if request.method == 'GET':
            try:
                print('nid',nid)
                # 根据nid 查询所在行的env_sub_node_id ，方便删除完跳转到具体详情页面
                db_node_id = models.DbInfo.objects.values('db_node_id').filter(db_id=nid)
                db_node_id = db_node_id[0].get('db_node_id')
                models.DbInfo.objects.filter(db_id=nid).delete()
            except Exception as e:
                pass
                # print(e)  #后期写到日志
            return redirect('/envManage/env/detail-%s' % db_node_id)
    else:
        return render(request,'login.html')


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
def envQuery(request):
    if request.session.get('is_login', None):
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
    else:
        return render(request,'login.html')


# 添加环境主信息
def envAdd(request):
    if request.session.get('is_login', None):
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
    else:
        return render(request, 'login.html')



# 添加环境详细服务信息
def envDetailAdd(request):
    if request.session.get('is_login', None):
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
    else:
        return render(request, 'login.html')

# 添加数据库详细服务信息
def dbDetailAdd(request):
    if request.session.get('is_login', None):
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
    else:
        return render(request, 'login.html')

# 主机管理
class Host(View):
    def get(self,request):
        if request.session.get('is_login',None):
            return render(request,'host.html')
        else:
            return render(request, 'login.html')

    def post(self,request):
        if request.session.get('is_login', None):
            intranetIP = request.POST.get('intranetIP')
            extrantIP = request.POST.get('extrantIP')
            serverType = request.POST.get('serverType')
            serverOs = request.POST.get('serverOs')

            queryConditions = {}
            if intranetIP:
                queryConditions['intranetIP'] = intranetIP
            if extrantIP:
                queryConditions['extrantIP'] = extrantIP
            if serverType:
                queryConditions['serverType'] = serverType
            if serverOs:
                queryConditions['serverOs'] = serverOs
            print("查询条件是：", queryConditions)

            if queryConditions:
                queryRes = models.ServerInfo.objects.filter(**queryConditions).all()
                list = []
                for i in queryRes:
                    data = {
                        'id': i.id,
                        'intranetIP': i.intranetIP,
                        'extrantIP': i.extrantIP,
                        'serverType': i.serverType,
                        'serverPurpose': i.serverPurpose,
                        'serverOs': i.serverOs,
                        'serverAccount': i.serverAccount,
                        'serverPassword': i.serverPassword,
                        'originServer': i.originServer
                    }
                    print('data', data)
                    list.append(data)
                return HttpResponse(json.dumps(list))  # string
            else:
                print("请求参数不存在！")
        else:
            return render(request,'login.html')

#数据管理
class Data(View):
    def get(self,request):
        if request.session.get('is_login', None):
            return render(request, 'data.html')
        else:
            return render(request, 'login.html')
    def post(self,request):
        if request.session.get('is_login', None):
            env = request.POST.get('env')
            cqmc = request.POST.get('cqmc')
            djlx = request.POST.get('djlx')
            xzxx = request.POST.getlist('xzxx')
            sfpl = request.POST.get('sfpl')
            print("请求参数是：",env,cqmc,djlx,xzxx,sfpl)

            res_msg = {'status': 0, 'data':None,'err_msg': None}
            if env and cqmc and djlx and sfpl:
                if cqmc == 'jd':
                    if djlx == 'dj_1':
                        if sfpl == 'y':
                            pass
                        else:
                            if not xzxx:
                                queryRes = sqlQuery.sqlQuery(env).getLandFirstRegisterData()
                                res_msg['data'] = queryRes
                            elif xzxx:
                                res_msg['status'] = 1
                                res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        if sfpl == 'y':
                            pass
                        else:
                            if not xzxx:
                                queryRes = sqlQuery.sqlQuery(env).getLandChangeRegisterData()
                                res_msg['data'] = queryRes
                            elif xzxx:
                                if len(xzxx) == 1:
                                    if xzxx[0] == 'sfdy':
                                        queryRes = sqlQuery.sqlQuery(env).getLandDyRegisterData()
                                        res_msg['data'] = queryRes
                                    elif xzxx[0] == 'sfcf':
                                        queryRes = sqlQuery.sqlQuery(env).getLandCfRegisterData()
                                        res_msg['data'] = queryRes
                                    else:
                                        res_msg['status'] = 1
                                        res_msg['err_msg'] = '选择限制信息不符合要求！'
                                elif len(xzxx) == 2:
                                    if 'sfdy' in xzxx and 'sfcf' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getLandDyAndCfRegisterData()
                                        res_msg['data'] = queryRes
                                    else:
                                        res_msg['status'] = 1
                                        res_msg['err_msg'] = '选择限制信息不符合要求！'
                                else:
                                    res_msg['status'] = 1
                                    res_msg['err_msg'] = '选择限制信息不符合要求！'
                        pass
                elif cqmc == 'fw':
                    if djlx == 'dj_1':
                        if sfpl == 'y':
                            # 首次批量
                            queryRes = sqlQuery.sqlQuery(env).getHouseFirstPlRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                            print("草拟吗",res_msg)
                        else:
                            if not xzxx:
                                queryRes = sqlQuery.sqlQuery(env).getHouseFirstRegisterData()
                                res_msg['data'] = queryRes
                            elif xzxx:
                                pass
                    else:
                        print('转移、变更、注销流程')
                        if sfpl == 'y':
                            pass
                        else:
                            if not xzxx:
                                queryRes = sqlQuery.sqlQuery(env).getHouseChangeRegisterData()
                                res_msg['data'] = queryRes
                                print('res_msg',res_msg)
                            elif xzxx:
                                if len(xzxx) == 1:
                                    # 抵押
                                    if xzxx[0] == 'sfdy':
                                        queryRes = sqlQuery.sqlQuery(env).getHouseDyRegisterData()
                                        res_msg['data'] = queryRes
                                    # 查封
                                    elif xzxx[0] == 'sfcf':
                                        queryRes = sqlQuery.sqlQuery(env).getHouseCfRegisterData()
                                        res_msg['data'] = queryRes
                                    # 异议
                                    elif xzxx[0] == 'sfyy':
                                        queryRes = sqlQuery.sqlQuery(env).getHouseYyRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg']='查无数据！'
                                        res_msg['data'] = queryRes
                                    # 预告（无预抵押）
                                    elif xzxx[0] == 'sfyg':
                                        queryRes = sqlQuery.sqlQuery(env).getHouseYgRegisterData()
                                        res_msg['data'] = queryRes
                                    else:
                                        res_msg['status'] = 1
                                        res_msg['err_msg'] = '选择限制信息不符合要求！'
                                elif len(xzxx) == 2:
                                    # 抵押+查封
                                    if 'sfdy' in xzxx and 'sfcf' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseDyAndCfRegisterData()
                                        res_msg['data'] = queryRes
                                    # 抵押+异议
                                    elif 'sfdy' in xzxx and 'sfyy' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseDyAndYyRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg'] = '查无数据！'
                                        res_msg['data'] = queryRes
                                    # 查封+异议
                                    elif 'sfyy' in xzxx and 'sfcf' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseCfAndYyRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg'] = '查无数据！'
                                        res_msg['data'] = queryRes
                                    # 预告+预抵押
                                    elif 'sfyg' in xzxx and 'sfydy' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseYgAndYdyRegisterData()
                                        res_msg['data'] = queryRes
                                    # 预告+预查封
                                    elif 'sfyg' in xzxx and 'sfycf' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseYgAndYcfRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg'] = '查无数据！'
                                        res_msg['data'] = queryRes
                                    else:
                                        res_msg['status'] = 1
                                        res_msg['err_msg'] = '选择限制信息不符合要求！'
                                elif len(xzxx) == 3:
                                    # 抵押+异议+查封
                                    if 'sfdy' in xzxx and 'sfcf' in xzxx and 'sfyy' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseDyAndYyAndCfRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg'] = '查无数据！'
                                        res_msg['data'] = queryRes
                                    # 预告+预抵押+预查封
                                    elif 'sfyg' in xzxx and 'sfydy' in xzxx and 'sfycf' in xzxx:
                                        queryRes = sqlQuery.sqlQuery(env).getHouseYgAndYdyAndYcfRegisterData()
                                        # 查无数据
                                        if queryRes == None:
                                            res_msg['status'] = 1
                                            res_msg['data'] = 'null'
                                            res_msg['err_msg'] = '查无数据！'
                                        res_msg['data'] = queryRes
                                else:
                                    res_msg['status'] = 1
                                    res_msg['err_msg'] = '选择限制信息不符合要求！'
                        pass
                elif cqmc == 'gjpt':
                    if djlx == 'dj_1':
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getGjptFirstRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getGjptChangeRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                elif cqmc == 'ck':
                    if djlx == 'dj_1':
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getCkFirstRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getCkChangeRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                elif cqmc == 'zjgc':
                    if xzxx:
                        if xzxx[0] == 'sfdy':
                            queryRes = sqlQuery.sqlQuery(env).getZjgcDyRegisterData()
                            res_msg['data'] = queryRes
                        elif xzxx[0] == 'sfcf':
                            queryRes = sqlQuery.sqlQuery(env).getZjgcCfRegisterData()
                            res_msg['data'] = queryRes
                        else:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        queryRes = sqlQuery.sqlQuery(env).getZjgcRegisterData()
                        res_msg['data'] = queryRes
                elif cqmc == 'zjfw':
                    if djlx == 'dj_1':
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getZjfwFirstRegisterData()
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        res_msg['status'] = 1
                        res_msg['err_msg'] = '选择登记类型不符合要求'
                elif cqmc == 'xmldz':
                    if djlx == 'dj_1':
                        if not xzxx:
                            queryRes = sqlQuery.sqlQuery(env).getXmldzFirstRegisterData()
                            # 查无数据
                            if queryRes == None:
                                res_msg['status'] = 1
                                res_msg['data'] = 'null'
                                res_msg['err_msg'] = '查无数据！'
                            res_msg['data'] = queryRes
                        elif xzxx:
                            res_msg['status'] = 1
                            res_msg['err_msg'] = '选择限制信息不符合要求'
                    else:
                        res_msg['status'] = 1
                        res_msg['err_msg'] = '选择登记类型不符合要求'
                else:
                    pass
            else:
                res_msg['err_msg'] = '部分查询条件必填缺失！'
            return HttpResponse(json.dumps(res_msg))
        else:
            return render(request,'login.html')
