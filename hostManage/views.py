from django.shortcuts import render,HttpResponse
from django.utils.decorators import method_decorator
from hostManage import models
from django.views import View
import json
from commonManage.views import getAuth,auth,hostInfoValidTemplate
from commonManage.logFunc import loggerConf
from commonManage.views import Page
logger = loggerConf().getLogger()

# 查询主机信息
@method_decorator(auth,name='dispatch')
class Host(View):
    def get(self,request):
        # 获取权限
        auth = getAuth(request.session.get('username'))
        return render(request,'host.html',{'auth':auth})

    def post(self, request):
        # 获取权限
        auth = getAuth(request.session.get('username'))


        intranetIP = request.POST.get('intranetIP')
        extrantIP = request.POST.get('extrantIP')
        serverType = request.POST.get('serverType')
        serverOs = request.POST.get('serverOs')

        # 根据前端传过来的不同条件加入到字典中
        queryConditions = {}
        if intranetIP:
            queryConditions['intranetIP'] = intranetIP
        if extrantIP:
            queryConditions['extrantIP'] = extrantIP
        if serverType:
            queryConditions['serverType'] = serverType
        if serverOs:
            queryConditions['serverOs'] = serverOs
        logger.debug("查询条件：%s" % queryConditions)

        # 将查询结果加入列表 返回给前端
        if queryConditions:
            queryHostRes = models.ServerInfo.objects.filter(**queryConditions).all()
            queryHostResToList = []
            for i in queryHostRes:
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
                logger.debug("查询结果：%s" % data)
                queryHostResToList.append(data)

            return render(request,'host.html',{'queryHostResToList':queryHostResToList,'auth':auth})
        else:
            logger.error("请求参数不存在！")

# 编辑主机信息
@auth
def hostEdit(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # id等获取前端传来的，其余字段可以从obj校验模板获取.obj封装前端需要校验的字段
        id = request.POST.get('s_id')
        serverPurpose = request.POST.get('serverPurpose')
        originServer = request.POST.get('originServer')
        extrantIP = request.POST.get('extrantIP')
        if extrantIP is '':
            extrantIP = None

        obj = hostInfoValidTemplate(request.POST)  # 将前端校验数据发给hostInfoValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                intranetIP = obj.cleaned_data.get('intranetIP')
                serverType = obj.cleaned_data.get('serverType')
                serverOs = obj.cleaned_data.get('serverOs')
                serverAccount = obj.cleaned_data.get('serverAccount')
                serverPassword = obj.cleaned_data.get('serverPassword')
                models.ServerInfo.objects.filter(id=id).update(
                    intranetIP=intranetIP,
                    extrantIP=extrantIP,
                    serverType=serverType,
                    serverOs=serverOs,
                    serverPurpose=serverPurpose,
                    originServer=originServer,
                    serverAccount=serverAccount,
                    serverPassword=serverPassword
                )
            except Exception as e:
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
                logger.error("请求异常：%s" % e)
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 添加主机信息
@auth
def hostAdd(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # id等获取前端传来的，其余字段可以从obj校验模板获取.obj封装前端需要校验的字段
        serverPurpose = request.POST.get('serverPurpose')
        originServer = request.POST.get('originServer')
        extrantIP = request.POST.get('extrantIP')
        logger.debug('extrantIP:', extrantIP)

        obj = hostInfoValidTemplate(request.POST)  # 将前端校验数据发给hostInfoValidTemplate模板,模板中定义的字段开始做校验
        v = obj.is_valid()
        if v:
            try:
                intranetIP = obj.cleaned_data.get('intranetIP')
                serverType = obj.cleaned_data.get('serverType')
                serverOs = obj.cleaned_data.get('serverOs')
                serverAccount = obj.cleaned_data.get('serverAccount')
                serverPassword = obj.cleaned_data.get('serverPassword')
                models.ServerInfo.objects.create(
                    intranetIP=intranetIP,
                    extrantIP=extrantIP,
                    serverType=serverType,
                    serverOs=serverOs,
                    serverPurpose=serverPurpose,
                    originServer=originServer,
                    serverAccount=serverAccount,
                    serverPassword=serverPassword
                )
            except Exception as e:
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
                logger.error("请求异常：%s" % e)
        else:
            res_msg['status'] = 1
            res_msg['err_msg'] = obj.errors
        return HttpResponse(json.dumps(res_msg))  # string

# 删除主机信息
@auth
def hostDel(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        hid = request.POST.get('hid')
        logger.debug('删除主机id为：%s' %hid)

        if hid:
            try:
                # 删除操作
                models.ServerInfo.objects.filter(id=hid).delete()
            except Exception as e:
                logger.error("请求异常：%s" %e)
                res_msg['status'] = 1
                res_msg['err_msg'] = '请求错误'
        else:
            logger.error("未获取到删除表主键id：%d" %hid)
            res_msg['status'] = 1
            res_msg['err_msg'] = '未获取到删除表主键id'
        return HttpResponse(json.dumps(res_msg))