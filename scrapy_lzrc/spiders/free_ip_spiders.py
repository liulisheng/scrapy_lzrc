# -*- coding:utf8 -*-
import scrapy

from scrapy_lzrc.FreeIp import FreeIp


class IpSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_lzrc.MysqlFreeIpPipeline.MysqlFreeIpPipeline': 2},

    }
    name = 'IpSpider'
    start_urls = ['https://www.kuaidaili.com/free/inha/2/']
    def parse(self, response):
        # 实例一个容器保存爬取的信息
        res=response.xpath('//*[@id="list"]/table/tbody/tr')
        for box in res:
            item = FreeIp()
            item['ip'] = box.xpath('.//td[1]/text()').extract()[0].strip() #职位
            item['port'] =box.xpath('.//td[2]/text()').extract()[0]
            yield item
