# -*- coding:utf8 -*-
# from scrapy_lzrc.settings import
import pymysql
from .settings import MYSQL_HOST
from .settings import MYSQL_DBNAME
from .settings import MYSQL_USER
from .settings import MYSQL_PASSWORD
class MysqlConcetion(object):
    host=MYSQL_HOST
    db=MYSQL_DBNAME
    user=MYSQL_USER
    password=MYSQL_PASSWORD
    def select(self,sql):
        try:
            # 打开数据库连接
            con = pymysql.connect(self.host,self.user,self.password,self.db )
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = con.cursor()
            num=cursor.execute(sql)
            if num<=1:
                result = cursor.fetchone()
            else:
                result= cursor.fetchall()
            # 关闭数据库连接
            con.close()
        except Exception as e:
           print(e)
        return result
    def update(self,sql):
        con = pymysql.connect(self.host,self.user,self.password,self.db )
        mycursor = con.cursor()
        mycursor.execute(sql)
        con.commit()
        con.close()