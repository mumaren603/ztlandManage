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