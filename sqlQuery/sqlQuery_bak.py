from common.dbExcute import DBAction
from conf import dbConf

class sqlQuery():
    def __init__(self,env):
        self.env = env
        self.db_qj_conn = DBAction(dbConf.dataBases.get(self.env).get('qj'))
        self.db_dj_conn = DBAction(dbConf.dataBases.get(self.env).get('dj'))

    # 净地首次登记数据
    def getLandFirstRegisterData(self):
        querySQL = "select bdcdyh,zddm,tdzl from KJK.dc_djdcbxx where zt='1' and sfyx='0' and tdzl>'0' and qllx='3' and bdcdyh >'0' and rownum < 30 order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据：",queryRes)
        # 检查该数据是否在登记平台做过登记,如果做过登记，发起流程会校验住，确保数据在权藉存在，在登记平台未做过登记
        queryJsydsyqSQL = "select count(1) from DJJGK.dj_jsydsyq where zt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        queryJsydsyqSQLRes = self.db_dj_conn.SqlExecute(queryJsydsyqSQL)
        print("登记平台数据条数为：%s" % queryJsydsyqSQLRes)
        if queryJsydsyqSQLRes[0]:
            print("登记平台该土地信息已登记，重新获取数据！")
            return sqlQuery(self.env).getLandFirstRegisterData()  # 递归
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 净地转移、变更、注销登记数据
    def getLandChangeRegisterData(self):
        querySQL = "select a.bdcdyh,a.zddm,a.zl,a.bdcqzh from (select djbid,bdcdyh,zddm,bdcqzh,zl from djjgk.dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getLandChangeRegisterData()  # 递归
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 净地抵押数据
    def getLandDyRegisterData(self):
        querySQL = "select a.bdcdyh,a.zddm,a.zl,a.bdcqzh from (select djbid,bdcdyh,zddm,zl,bdcqzh from djjgk.dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 1 and sfcf = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id inner join(select djbid from djjgk.dj_dy_djben_zm where sfyx=1 and sfdy=1 )c on a.djbid = c.djbid and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getLandDyRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 净地查封数据
    def getLandCfRegisterData(self):
        querySQL = "select  a.bdcdyh,a.zddm,a.zl,a.bdcqzh from (select bdcdyh,zddm,bdcqzh,zl,id,djbid from djjgk.dj_jsydsyq where zt='1' and sfyx=1)a inner join (select cqbid,djbid from djjgk.dj_cf where zt='1' and sfyx=1)b on a.id=b.cqbid inner join (select id from djjgk.dj_djben where zt='1' and sfyx=1)c on a.djbid=c.id where a.bdcdyh > '0' and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getLandCfRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 净地抵押和查封数据
    def getLandDyAndCfRegisterData(self):
        querySQL="select distinct bdcdyh,zddm,zl,bdcqzh from (select djbid,bdcdyh,zddm,bdcqzh,zl from djjgk.dj_jsydsyq where qllx='3' and zt='1' and sfyx=1 and bdcdyh not like '%9999%') a inner join (select id from djjgk.dj_djben where sfdy=1 and sfcf=1 and sfysczql=1 and zt='1' and sfyx=1) b on a.djbid=b.id inner join (select djbid from dj_dy where zt='1' and sfyx=1)c on b.id = c.djbid inner join (select djbid from dj_cf where zt='1' and sfyx=1)d on b.id = d.djbid and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getLandDyAndCfRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    ####################房屋产权查询#####################
    # 商品房首次登记数据
    def getHouseFirstRegisterData(self):
        querySQL = "select a.bdcdyh,a.fwbh as fwdm,a.zl from (select bdcdyh, fwbh, zl,lszfwbh from kjk.dc_h_fwzk where zt = '1' and sfyx = '0' and fwyt1 > '0' and scjzmj > '0' and bdcdyh like '%GB%' and (fwlx = '1' or fwlx = '2' or fwlx = '3' or fwlx = '4' or fwlx = '99'))a left join (select fwbh from kjk.dc_h where zt = '1' and bdcdyh > '0') b on a.fwbh = b.fwbh left join (select zddm, fwbh from kjk.dc_z where zt = '1') c on a.lszfwbh = c.fwbh inner join (select zddm from kjk.dc_djdcbxx where zt = '1' and sfyx = '1') d on c.zddm = d.zddm where rownum <50  order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        if querySqxxSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseFirstRegisterData()  # 递归
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋转移、变更、注销登记数据
    def getHouseChangeRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from (select bdcdyh,fwdm,fwzl,bdcqzh,djbid from dj_fdcq2 a where a.qllx=4 and a.zt=1 and a.sfyx=1 and a.bdcdyh not like '%9999%' and a.fwxz='0') a inner join (select id from dj_djben b where b.sfdy=0 and b.sfcf=0 and b.sfyg=0 and b.sfysczql=1 and b.zt=1 and b.sfyx=1) b on a.djbid=b.id and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseChangeRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    ##############批量###################
    
    # 自建房屋首次登记
    def getZjfwFirstRegisterData(self):
        querySQL = "select a.bdcdyh,a.fwbh as fwdm,a.zl from （select bdcdyh, fwbh, zl,lszfwbh from dc_h_fwzk where zt = '1' and sfyx = '0' and fwlx = '1' or fwlx = '2' or fwlx = '3'  or fwlx = '4' or fwlx='5' or fwlx='99') a inner join (select fwbh from dc_h where zt = '1') b on a.fwbh = b.fwbh inner join （select fwbh,zddm from dc_z where zt = '1') c on a.lszfwbh = c.fwbh inner join (select zddm from dc_djdcbxx where zt = '1' and sfyx = '1') d on c.zddm = d.zddm where rownum<50 order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据为：" , queryRes)
        # 检查该数据是否存在待办
        querySqxxSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        if querySqxxSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getZjfwFirstRegisterData()  # 递归
        else:
            print("数据符合！数据为：" , queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 公建配套首次登记数据
    def getGjptFirstRegisterData(self):
        querySQL="select distinct c.bdcdyh,c.zddm,c.mph as zl from （select lszfwbh,bdcdyh,fwbh,zl from kjk.dc_h_fwzk where zt = '1' and sfyx = '0' and (fwlx = '9901' or fwlx = '99')) a left join (select fwbh from kjk.dc_h where zt = '1' and bdcdyh>'0') b on a.fwbh = b.fwbh left join （select fwbh,zddm,bdcdyh,mph from kjk.dc_z where zt = '1') c on a.lszfwbh = c.fwbh left join (select zddm,bdcdyh from kjk.dc_djdcbxx where zt = '1' and sfyx = '1') d on c.zddm = d.zddm where d.bdcdyh > '0' and rownum <50  order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据为：" , queryRes)
        if queryRes[0] != None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from ywbdk.yw_sqxxzb where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getGjptFirstRegisterData()
            else:
                print("数据符合！数据为：" , queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 车库位首次登记数据
    def getCkFirstRegisterData(self):
        querySQL="select c.bdcdyh,c.zddm,c.mph as zl from " \
                 "(select bdcdyh,zl,fwbh,lszfwbh,fwlx  from dc_h_fwzk  where zt = '1' and sfyx = '0'  and fwyt1 != '84' and fwyt1 != '54' and fwyt1 != '22' and fwyt1 != '8401') a " \
                 "left join (select fwbh from dc_h where zt = '1') b on a.fwbh = b.fwbh " \
                 "left join (select bdcdyh,fwbh,mph,zddm from dc_z where zt = '1') c  on a.lszfwbh = c.fwbh " \
                 "left join (select zddm from dc_djdcbxx where zt = '1'and sfyx = '1') d on c.zddm = d.zddm " \
                 "where 1 = 1 and (a.FWLX = '6' or a.FWLX = '9902' or a.FWLX = '99') and rownum<50"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据为：" , queryRes)
        if queryRes[0] != None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from ywbdk.yw_sqxxzb where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getCkFirstRegisterData()
            else:
                print("数据符合！数据为：" , queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 项目类多幢首次登记数据
    def getXmldzFirstRegisterData(self):
        querySQL="select distinct a.bdcdyh,a.fwbh as fwdm,a.zl from (select bdcdyh,fwbh,zl,lszfwbh,fwlx from dc_h_fwzk where zt = '1'and sfyx = '0') a left join (select fwbh from dc_h where zt = '1') b on a.fwbh = b.fwbh left join (select fwbh,zddm from dc_z where zt = '1') c on a.lszfwbh = c.fwbh left join (select zddm from kjk.dc_djdcbxx where zt = '1'and sfyx = '1') d on c.zddm = d.zddm where 1 = 1 and a.bdcdyh > '0' and (a.fwlx = 1 or a.fwlx = 2 or a.fwlx = 3 or a.fwlx = 4 or a.fwlx = 5 or a.fwlx = 99) and rownum <50 order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("权籍查询数据为：" , queryRes)
        if queryRes != None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from ywbdk.yw_sqxxzb where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getXmldzFirstRegisterData()
            else:
                print("数据符合！数据为：" , queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 在建工程首次数据(无抵押，查封)
    def getZjgcRegisterData(self):
        querySQL = "select distinct c.bdcdyh,c.zddm,c.mph as zl from (" \
                   "select fwbh,lszfwbh from kjk.dc_ych_fwzk where zt = '1'and sfyx = '0') a " \
                   "left join (select fwbh from kjk.dc_ych where zt = '1'and bdcdyh > '0') b on a.fwbh = b.fwbh " \
                   "left join (select fwbh,zddm,bdcdyh,mph from kjk.dc_ycz where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh left join " \
                   "(select zddm from kjk.dc_djdcbxx where zt = '1' and sfyx = '1') d on c.zddm = d.zddm " \
                   "where c.bdcdyh > '0' and rownum <50 order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getZjgcRegisterData()  # 递归
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 在建工程抵押数据
    def getZjgcDyRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.zl from (select bdcdyh,fwdm,zl,djbid from dj_zjgcdy where zt='1' and sfyx=1 and bdcdyh not like '%9999%') a inner join (select id from dj_djben where sfzjgcdy=1 and sfcf=0 and sfyy=0 and sfzzdj=0 and sfzjgccf=0 and zt=1 and sfyx=1) b on a.djbid=b.id  where rownum <50"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getZjgcDyRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 在建工程查封数据
    def getZjgcCfRegisterData(self):
        querySQL = "select  distinct a.bdcdyh,a.fwdm,a.zl from (select bdcdyh,fwdm,zl,djbid from dj_zjgccf where zt='1' and sfyx=1) a inner join (select id from dj_djben where sfzjgccf=1 and sfcf=0 and zt=1 and sfyx=1) b on a.djbid=b.id  where  bdcdyh > '0' and rownum <50"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getZjgcCfRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋抵押数据
    def getHouseDyRegisterData(self):
        querySQL="select a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from (select djbid,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2 where zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 1 and sfcf = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id inner join(select djbid from djjgk.dj_dy_djben_zm where sfyx=1 and sfdy=1 )c on a.djbid = c.djbid and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseDyRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋查封数据
    def getHouseCfRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from (select djbid,id,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2  where zt='1' and sfyx=1) a inner join (select id from djjgk.dj_djben b where sfdy=0 and sfcf=1 and sfyg=0 and zt='1'and sfyx=1) b on a.djbid=b.id inner join (select cqbid from dj_cf where cfwj>'0' and cfwh>'0' and cflxmc = '查封' and zt='1' and sfyx=1) c on a.id = c.cqbid where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseCfRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋异议数据
    def getHouseYyRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from (select id,bdcdyh,djbid,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2  where zt='1' and sfyx=1) a inner join (select id from djjgk.dj_djben b where sfdy=0 and sfcf=0 and sfyg=0 and sfyy=1 and zt='1'and sfyx=1) b on a.djbid=b.id inner join (select cqbid from dj_yy where zt='1' and sfyx=1) c on a.id = c.cqbid where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes != None:
        # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getHouseYyRegisterData()
            else:
                print("数据符合！数据为：" ,queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 房屋预告数据
    def getHouseYgRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.zl,a.bdcdjzmh from (select bdcdyh,fwdm,zl,bdcdjzmh,djbid from djjgk.dj_yg  where zt='1' and sfyx=1) a inner join (select id from djjgk.dj_djben b where sfyg=1 and sfycf=0 and sfydy=0 and sfysczql=0 and zt='1'and sfyx=1) b on a.djbid=b.id where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseYgRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋抵押+查封数据
    def getHouseDyAndCfRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from " \
                   "(select djbid,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh not like '%9999%') a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben where sfdy=1 and sfcf=1 and zt='1' and sfyx=1) b" \
                   " on a.djbid=b.id where rownum<20 "
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseDyAndCfRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋抵押+异议数据
    def getHouseDyAndYyRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from " \
                   "(select djbid,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh not like '%9999%') a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben where sfdy=1 and sfyy=1  and sfcf=0 and zt='1' and sfyx=1) b" \
                   " on a.djbid=b.id where rownum<20 "
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes != None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getHouseDyAndYyRegisterData()
            else:
                print("数据符合！数据为：" ,queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 房屋查封+异议数据
    def getHouseCfAndYyRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from " \
                   "(select djbid,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh not like '%9999%') a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben where sfyy=1 and sfcf=1  and sfdy=0 and zt='1' and sfyx=1) b" \
                   " on a.djbid=b.id where rownum<20 "
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("数据符合！数据为：" ,queryRes)
                return sqlQuery(self.env).getHouseCfAndYyRegisterData()
            else:
                print("数据符合！数据为：%s" % queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 房屋预告+预抵押数据
    def getHouseYgAndYdyRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.zl,a.bdcdjzmh from " \
                   "(select bdcdyh,fwdm,bdcdjzmh,zl,djbid from djjgk.dj_yg  where zt='1' and sfyx=1) a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben b where sfyg=1 and sfydy=1 and sfycf=0 and zt='1'and sfyx=1) b" \
                   " on a.djbid=b.id " \
                   "where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
            print("该数据已在办理中，重新获取数据！")
            return sqlQuery(self.env).getHouseYgAndYdyRegisterData()
        else:
            print("数据符合！数据为：" ,queryRes)
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 房屋预告+预查封数据
    def getHouseYgAndYcfRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.zl,a.bdcdjzmh from " \
                   "(select bdcdyh,fwdm,bdcdjzmh,zl,djbid from djjgk.dj_yg  where zt='1' and sfyx=1) a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben b where sfyg=1 and sfycf=1 and sfydy=0 and zt='1'and sfyx=1) b" \
                   " on a.djbid=b.id " \
                   "where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes !=None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getHouseYgAndYcfRegisterData()
            else:
                print("数据符合！数据为：" ,queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 房屋抵押+异议+查封数据
    def getHouseDyAndYyAndCfRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.fwzl,a.bdcqzh from " \
                   "(select djbid,bdcdyh,fwdm,fwzl,bdcqzh from djjgk.dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh not like '%9999%') a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben where sfdy=1 and sfcf=1 and sfyy=1 and zt='1' and sfyx=1) b" \
                   " on a.djbid=b.id where rownum<20 "
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes != None:
        # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getHouseDyAndYyAndCfRegisterData()
            else:
                print("数据符合！数据为：" ,queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    # 房屋预告+预抵押+预查封数据
    def getHouseYgAndYdyAndYcfRegisterData(self):
        querySQL = "select distinct a.bdcdyh,a.fwdm,a.zl,a.bdcdjzmh from " \
                   "(select bdcdyh,fwdm,bdcdjzmh,zl,djbid from djjgk.dj_yg  where zt='1' and sfyx=1) a " \
                   "inner join " \
                   "(select id from djjgk.dj_djben b where sfyg=1 and sfycf=1 and sfydy=1 and zt='1'and sfyx=1) b" \
                   " on a.djbid=b.id " \
                   "where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        print("DJJGK查询数据：" ,queryRes)
        if queryRes != None:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes[0] + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes[0] + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes[0] or querySqxxzbSQLRes[0]:
                print("该数据已在办理中，重新获取数据！")
                return sqlQuery(self.env).getHouseYgAndYdyAndYcfRegisterData()
            else:
                print("数据符合！数据为：" ,queryRes)
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            return

    #公建配套产权查询
    def gjptCqQuery(self):
        pass

    #在建工程产权查询
    def zjgcCqQuery(self):
        pass