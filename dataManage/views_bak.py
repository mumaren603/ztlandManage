from django.shortcuts import render, HttpResponse
from django.views import View
import json
from commonManage import sqlQuery


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
