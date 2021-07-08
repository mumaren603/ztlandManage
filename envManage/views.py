from django.shortcuts import render,redirect,HttpResponse
from django.utils.decorators import method_decorator
from envManage import models
from django.views import View
from commonManage.views import envDetailInfoValidTemplate,envValidTemplate,dbDetailInfoValidTemplate
import json
from commonManage.views import getAuth,auth
from commonManage.views import Page
from commonManage.logFunc import loggerConf

logger = loggerConf().getLogger()


'''环境主信息操作'''
# 获取主信息
@auth
def env(request):
    if request.method == 'GET':
        envInfo = models.EnvInfo.objects.all()
        if envInfo:
            logger.debug("主环境信息：%s" %envInfo)
        else:
            logger.error("未查询到主环境信息")

        # 获取权限
        auth = getAuth(request.session.get('username'))

        # 获取数据总条数
        env_count = len(envInfo)
        logger.debug("环境信息总条数是：%d" % env_count)
        # print("环境信息总条数是：%d" % env_count)

        # 获取当前页码
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)

        # 定义每页展示数据条数
        val = request.COOKIES.get('per_page_count', 8)
        val = int(val)

        # 调用Page类实现页码动态展示
        page_obj = Page(current_page, env_count, val)

        envInfo = envInfo[page_obj.start:page_obj.end]
        # print('当前页码对应的数据为：%s' %envInfo)
        logger.debug('当前页码对应的数据为：%s' %envInfo)

        page_str = page_obj.page_str("/envManage/env")

        return render(request,'env.html',{'envinfo':envInfo,'auth':auth,'page_str':page_str})
    else:
        return render(request, 'login.html')

# 添加环境主信息
@auth
def envAdd(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # status获取前端传来的，其余字段可以从obj获取.obj封装前端需要校验的字段
        status = request.POST.get('status')

        obj = envValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
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
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
                logger.error("请求异常：%s" %e)
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 编辑环境主信息
@auth
def envEdit(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # id，status获取前端传来的，其余字段可以从obj获取.obj封装前端需要校验的字段
        id = request.POST.get('s_id')
        status = request.POST.get('status')

        obj = envValidTemplate(request.POST)  # 将前端校验数据发给addEnvValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                frontIP = obj.cleaned_data.get('frontIP')
                backIP = obj.cleaned_data.get('backIP')
                dbIP = obj.cleaned_data.get('dbIP')
                env_name = obj.cleaned_data.get('env_name')
                models.EnvInfo.objects.filter(m_id=id).update(
                    frontIP=frontIP,
                    backIP=backIP,
                    dbIP=dbIP,
                    env_name=env_name,
                    status=status
                )
            except Exception as e:
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
                logger.error("请求异常：%s" % e)
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 删除环境主信息
@auth
def envDel(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        hid = request.POST.get('hid')
        logger.debug('删除主环境id为：%s' %hid)

        if hid:
            try:
                # 这部分主要为了记录删除数据到日志中
                obj = models.EnvDetailInfo.objects.filter(env_sub_node_id=hid).values()
                logger.debug("删除前EnvDetailInfo表中存在%d条数据" %len(obj))

                if len(obj)>0:
                    for row in obj:
                        logger.debug("删除数据为%s" %row)

                # 删除操作
                models.EnvDetailInfo.objects.filter(env_sub_node_id=hid).delete()

                del_obj = models.EnvDetailInfo.objects.filter(env_sub_node_id=hid).values()
                logger.debug("EnvDetailInfo表数据删除结束，表中存在%d条数据" %len(del_obj))
                # 子表数据删除完则执行主表数据删除
                if not del_obj:
                    models.EnvInfo.objects.filter(m_id=hid).delete()
                else:
                    raise Exception
                    logger.debug("删除失败，错误信息为:%s" %Exception)
                    res_msg['status'] = 1
                    res_msg['err_msg'] = '请求错误'
            except Exception as e:
                logger.error("请求异常：%s" %e)
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = '未获取到删除表主键id'
        return HttpResponse(json.dumps(res_msg))

# 查询环境主信息(非ajax)
@auth
def envQuery(request):
    if request.method == 'GET':
        logger.error('不支持请求方式-->GET')
        return redirect('/common/login')

    if request.method == 'POST':
        queryParam = request.POST.get('searchParam')
        logger.debug("查询环境信息条件：%s" % queryParam)

        # 获取权限
        auth = getAuth(request.session.get('username'))

        if queryParam:
            try:
                # 环境信息支持模糊查询
                queryRes = models.EnvInfo.objects.filter(env_name__contains=queryParam).first()
                logger.debug("查询环境信息结果：%s" % queryRes)
                return render(request, 'envQuery.html', {'queryRes':queryRes,'auth':auth})
            except Exception as e:
                raise e
                logger.error("查询错误：%s" %e)
        else:
            return HttpResponse('请求错误')

'''环境详细信息'''
# @auth
# def envDetail(request, nid):
#     if request.method == 'GET':
#         # 获取权限
#         auth = getAuth(request.session.get('username'))
#
#         # 数据处理
#         envNode = models.EnvInfo.objects.filter(m_id=nid).first()
#         print('envNode',envNode)
#         # 根据nid,查询出该环境前端、微服务、FTP
#         frontService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid, service_model='前端')
#         backService = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid, service_model='后端')
#         microService = models.EnvDetailInfo.objects.filter(env_sub_node=nid, service_model='微服务')
#         FtpService = models.EnvDetailInfo.objects.filter(env_sub_node=nid, service_model='FTP')
#         dbService = models.DbInfo.objects.filter(db_node_id=nid)
#
#         # 获取数据总条数
#         env_count = models.EnvDetailInfo.objects.filter(env_sub_node_id=nid, service_model='后端').count()
#         print("后端环境信息总条数是：%d" % env_count)
#
#         # 获取当前页码
#         current_page = request.GET.get('p', 1)
#         current_page = int(current_page)
#
#         # 定义每页展示数据条数
#         val = request.COOKIES.get('per_page_count', 8)
#         val = int(val)
#
#         # 调用Page类实现页码动态展示
#         page_obj = Page(current_page, env_count, val)
#         print('page_obj', page_obj)
#
#         backService = backService[page_obj.start:page_obj.end]
#         print('当前页码对应的数据为：%s' % backService)
#
#         page_str = page_obj.page_str("/envManage/env/detail-%s" % nid)
#
#
#         # 返回信息有前端传过来入参nid? 主页面传过来参数便于子页面添加数据时和主页面数据关联
#         return render(request, 'envDetail-1.html',
#                       {'auth': auth, 'env_node_id': nid, 'envNode': envNode, 'frontService': frontService,
#                        'backService': backService, 'microService': microService, 'FtpService': FtpService,
#                        'dbService': dbService,'page_str': page_str})
#     else:
#         return render(request, 'login.html')

'''环境详细信息
@param request: 前端所有请求
@param nid:前端传过来主环境信息id
@param uid:取值（1，2，3，4，5）分别对应前端，后端，中间件，FTP，数据库
'''
class envDetail(View):
    @method_decorator(auth)
    def get(self,request,nid,uid):
        self.nid = nid
        self.uid = uid
        print('nid:',nid)
        print('uid:', uid)

        # 获取权限
        auth = getAuth(request.session.get('username'))

        # 前端数据
        if self.uid == '1':
            frontService = self.getFrontService()
            logger.debug("前端返回所有数据:%s" % frontService)

            data,page_str = self.getPage(request,self.nid,self.uid,frontService)
            frontService = data

            return render(request, 'envDetail-1.html', {'auth': auth, 'env_node_id': nid,  'frontService': frontService,'page_str':page_str})
        # 后端数据
        elif self.uid == '2':
            backService = self.getBackService()
            logger.debug("后端返回所有数据:%s" % backService)

            data,page_str = self.getPage(request,self.nid,self.uid,backService)
            backService = data

            return render(request, 'envDetail-2.html',{'auth': auth, 'env_node_id': nid,'backService': backService,'page_str':page_str})
        # 中间件数据
        elif self.uid == '3':
            middleService = self.getMiddleService()
            logger.debug("中间件返回所有数据:%s" % middleService)
            # print("中间件返回所有数据：",middleService)

            data,page_str = self.getPage(request,self.nid,self.uid,middleService)
            middleService = data

            return render(request, 'envDetail-3.html',{'auth': auth, 'env_node_id': nid,'middleService': middleService,'page_str':page_str})
        # Ftp数据
        elif self.uid == '4':
            ftpService = self.getFtpService()
            logger.debug("FTP返回所有数据:%s" % ftpService)
            # print("FTP返回所有数据：", ftpService)

            data,page_str = self.getPage(request,self.nid,self.uid,ftpService)
            ftpService = data

            return render(request, 'envDetail-4.html',{'auth': auth, 'env_node_id': nid, 'ftpService': ftpService,'page_str':page_str})
        # 数据库数据
        elif self.uid == '5':
            dbService = self.getDbService()
            logger.debug("数据库返回所有数据:%s" % dbService)
            # print("数据库返回所有数据：", dbService)

            data,page_str = self.getPage(request,self.nid,self.uid,dbService)
            dbService = data

            return render(request, 'envDetail-5.html',{'auth': auth, 'env_node_id': nid, 'dbService': dbService,'page_str':page_str})


    def getFrontService(self):
        frontService = models.EnvDetailInfo.objects.filter(env_sub_node_id=self.nid, service_model='前端')
        return frontService

    def getBackService(self):
        backService = models.EnvDetailInfo.objects.filter(env_sub_node_id=self.nid, service_model='后端')
        return backService

    def getMiddleService(self):
        middleService = models.EnvDetailInfo.objects.filter(env_sub_node=self.nid, service_model='中间件')
        return middleService

    def getFtpService(self):
        ftpService = models.EnvDetailInfo.objects.filter(env_sub_node=self.nid, service_model='FTP')
        return ftpService

    def getDbService(self):
        dbService = models.DbInfo.objects.filter(db_node_id=self.nid)
        return dbService

    # 分页公共方法
    def getPage(self,request,nid,uid,node):
        # 分页
        # 获取数据总条数
        env_count = len(node)
        logger.debug("查询数据库信息总条数：%d" % env_count)
        # print("查询数据库信息总条数：%d" % env_count)

        # 获取当前页码
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        logger.debug('当前页码是：%d' % current_page)
        # print('当前页码是：%d' % current_page)

        # 定义每页展示数据条数
        val = request.COOKIES.get('per_page_count', 8)
        val = int(val)

        # 调用Page类实现页码动态展示
        page_obj = Page(current_page, env_count, val)

        data = node[page_obj.start:page_obj.end]
        logger.debug('当前页码对应的数据为：%s' % data)
        # print('当前页码对应的数据为：%s' % data)

        page_str = page_obj.page_str("/envManage/env/detail-%s-%s" % (nid, uid))
        return data,page_str

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
                logger.error("异常信息：%s" %e)
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
                logger.error("异常信息：%s" % e)
                # print(e)                  #后期处理成记录到日志
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 环境、数据库详细信息删除确定
class envDetaildel(View):
    def get(self,request):
        pass

    @method_decorator(auth)
    def post(self,request):
        res_msg = {'status': 0, 'err_msg': None}

        hid = request.POST.get('hid')
        node = request.POST.get('node')
        logger.debug('删除详细环境信息id为：%s' %hid)
        logger.debug('删除信息所属node为：%s' %node)

        # print('删除详细环境信息id为：',hid)
        # print('删除信息所属node为：', node)
        if hid:
            if node:
                try:
                    models.EnvDetailInfo.objects.filter(s_id=hid).delete()
                except Exception as e:
                    logger.debug('删除失败，错误信息是:%s' %e)
                    # print('删除失败，错误信息是', e)
                    res_msg['status'] = 1
                    res_msg['err_msg'] = '请求错误'
            else:
                try:
                    models.DbInfo.objects.filter(db_id=hid).delete()
                except Exception as e:
                    logger.debug('删除失败，错误信息是:%s' % e)
                    # print('删除失败，错误信息是', e)
                    res_msg['status'] = 1
                    res_msg['err_msg'] = '请求错误'
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = '未获取到删除表主键id'
        return HttpResponse(json.dumps(res_msg))

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
                logger.error("异常信息：%s" %e)
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
                logger.error("异常信息：%s" %e)
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

