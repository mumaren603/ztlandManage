from django.shortcuts import render,HttpResponse
from django.utils.decorators import method_decorator
from hostManage import models
from django.views import View
import json
from commonManage.views import getAuth,auth

# 主机管理
@method_decorator(auth,name='dispatch')
class Host(View):
    def get(self,request):
        return render(request,'host.html')

    def post(self, request):
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
