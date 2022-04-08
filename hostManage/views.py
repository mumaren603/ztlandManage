import json
import xlwt
from io import BytesIO
from hostManage import models
from django.views import View
from django.shortcuts import render,HttpResponse
from django.utils.decorators import method_decorator
from commonManage.views import getAuth,auth,hostInfoValidTemplate
from commonManage.logFunc import loggerConf
from commonManage.excelStyle import xlsStyleSet
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

        # 获取前端请求参数
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
            if queryHostRes:
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
                return render(request, 'host.html', {'queryHostResToList': queryHostResToList, 'auth': auth})
            else:
                pass  # 查无数据
        else:
            logger.error("请求参数不存在！")

# 编辑主机信息
@auth
def hostEdit(request):
    if request.method == 'POST':
        res_msg = {'status': 0, 'err_msg': None}

        # id等字段获取前端传来的，其余字段可以从obj校验模板获取.obj封装前端需要校验的字段
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

# 导出主机信息
@auth
def hostExport(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;'

    """导出excel表"""
    # 创建工作簿
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet('主机信息')

    # 设置EXCEL单元格样式（主要是长宽高）
    for i in range(9):
        col_set = w.col(i)
        if i == 0:  # 序号 宽度设置偏小  其他单元格格式宽度一致
            col_set.width = 256 * 8
        else:
            col_set.width = 256 * 18

    # 创建样式对象
    style_head = xlsStyleSet(align_horz=0x01,align_vert=0x01,font_bold=True,font_height=20*15).getStyle()
    style_body = xlsStyleSet(align_horz=0x01,align_vert=0x01,font_height=20*13).getStyle()

    host_info = models.ServerInfo.objects.values_list('intranetIP', 'extrantIP', 'serverOs','serverAccount', 'serverPassword','serverType','serverPurpose','originServer')
    if host_info:
        # 写入表头
        w.write(0, 0, u'序号', style_head)
        w.write(0, 1, u'内网IP', style_head)
        w.write(0, 2, u'外网IP', style_head)
        w.write(0, 3, u'操作系统', style_head)
        w.write(0, 4, u'用户名', style_head)
        w.write(0, 5, u'密码', style_head)
        w.write(0, 6, u'机器类型', style_head)
        w.write(0, 7, u'机器用途', style_head)
        w.write(0, 8, u'宿主机', style_head)

        # 写入内容
        # 行号
        row_num = 1
        # 序号
        order_num = 1
        for row in host_info:
            w.write(row_num, 0, order_num, style_body)
            w.write(row_num, 1, row[0], style_body)
            w.write(row_num, 2, row[1], style_body)
            w.write(row_num, 3, row[2], style_body)
            w.write(row_num, 4, row[3], style_body)
            w.write(row_num, 5, row[4], style_body)
            w.write(row_num, 6, row[5], style_body)
            w.write(row_num, 7, row[6], style_body)
            w.write(row_num, 8, row[7], style_body)
            row_num += 1
            order_num += 1
        # 写出到IO
        output = BytesIO()
        ws.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())

    return response
