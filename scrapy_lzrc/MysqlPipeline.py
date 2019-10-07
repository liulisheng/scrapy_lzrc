# -*- coding:utf8 -*-
import pymysql as pymysql
from twisted.enterprise import adbapi
from urllib.request import urlretrieve
import os
from PIL import Image
import pytesseract
from .settings import IMAGES_STORE

class MysqlPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
        self.path = IMAGES_STORE #图片保存路径
        self.page = 0 #图片名我用数字代替
        if not os.path.exists(self.path): #检查文件是否存在
            os.mkdir(self.path)

    def question(self,a,b,c):	#附赠一个观察下载进度的函数方法，当然也可以不调用
        per = 100*a*b/c 		#在方法一中调用
        if per>=100:
            per = 100
            print("下载完成！！")
        print("%.2f%%" % per)

    @classmethod
    def from_settings(cls,settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self,item,spider):

        # src = item['phone']
        # strStr=src.split('/')
        # try:				#下载图片方法一，在使用urlretrieve直接下载，这个代码量少
        #     print(self.path+"%s.png"%strStr[-1])
        #     urlretrieve(src,self.path+"%s.png"%strStr[-1],self.question)
        #     phone=pytesseract.image_to_string(Image.open(self.path+"%s.png"%strStr[-1]))
        #     print('phone：'+phone)
        #     if phone:
        #         item['phone']=phone
        # except Exception as e:
        #     print(e)

        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert,item)
        # 添加异常处理
        query.addCallback(self.handle_error)

    def do_insert(self,cursor,item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
                INSERT INTO `tb_gxrc_zp`(`company`, `url`, `pos_name`, `salary`, `workplace`, `update_time`, `education`, `num`, `experience`, `contact_name`, `phone`, `e_mail`, `address`,`company_type`) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    """
        cursor.execute(insert_sql,(item['company'], item['url'],item['posName'], item['salary'],item[ 'workplace'],item[ 'updateTime'],item[ 'education'],
                                    item['num'], item['experience'],item[ 'contact_name'],item[ 'phone'], item['e_mail'], item['address'], item['companyType']))
        return item

    def handle_error(self,failure):
        if failure:
            # 打印错误信息
            print(failure)