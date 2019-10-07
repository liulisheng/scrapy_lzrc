# -*- coding:utf8 -*-
import scrapy
# 编写model模板
class FreeIp(scrapy.Item):
    ip = scrapy.Field() #ip
    port=scrapy.Field() #端口