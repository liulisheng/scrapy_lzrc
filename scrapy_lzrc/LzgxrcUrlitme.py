# -*- coding:utf8 -*-
import scrapy
# 编写model模板
class LzgxrcUrlitme(scrapy.Item):
    # 储存标题
    company = scrapy.Field() #公司名称
    companyType= scrapy.Field() #公司性质
    url = scrapy.Field()     #url
    posName=scrapy.Field()   #职位
    salary=scrapy.Field()    #薪资
    workplace=scrapy.Field() #工作地
    updateTime=scrapy.Field() #更新时间
    education=scrapy.Field() #学历
    num=scrapy.Field() #人数
    experience=scrapy.Field() #经验

    contact_name = scrapy.Field()    #联系人
    phone = scrapy.Field()  #电话
    e_mail = scrapy.Field()  #email
    address = scrapy.Field() #地址

