# -*- coding:utf8 -*-
import time

import scrapy
# 引入本地的模板
from scrapy import FormRequest



from scrapy_lzrc.LzgxrcUrlitme import LzgxrcUrlitme


class MyScr(scrapy.Spider):

    # 设置全局唯一的name
    name = 'lz_gxrc_scr_url'
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_lzrc.MysqlPipeline.MysqlPipeline': 1},
    }
    # 先从
    #//*[@id="posList"]/div[20]/ul[1]/li[2]/a 爬取公司名称  company
    #//*[@id="posList"]/div[20]/ul[1]/li[2]/a/@href 拿到各个公司的详情页地址 div[2]列表第几条记录
    #进入详情页爬取详情
    #联系人 //*[@id="address"]/table/tbody/tr[2]/td  name
    #联系电话 //*[@id="address"]/table/tbody/tr[3]/td/img/@src  phone
    #e_mail //*[@id="address"]/table/tbody/tr[6]/td   e_mail
    #联系地址 //*[@id="address"]/table/tbody/tr[1]/td  address

    allowed_domains = ["s.gxrc.com"]

    headers ={
        "authority": "s.gxrc.com",
        ":method": "GET",
        ":path": "/WebPage/AjaxLogin.aspx?showSata=1&randon=0.8016450752555082",
        ":scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie":"UM_distinctid=16b82a522788c6-053f2aa7b72273-123e6e57-13c680-16b82a5227980c; Hm_lvt_8b5e38a6a547f78d5f305bf6658222cd=1561264989; CNZZDATA1260243366=1821447571-1561263881-http%253A%252F%252Fwww.gxrc.com%252F%7C1561263881; Hm_lvt_f02e7d4aa064a3a8d36ae3d94b01a1ed=1561264993; searchLog=[{k:\"java\",t:\"1\"}]; BIGipServernss-gxrc-11=202096812.22528.0000; Hm_lvt_c0560399b847a97bd18c2e2551860d9e=1569385667,1569394346; Hm_lpvt_c0560399b847a97bd18c2e2551860d9e=1569397510; CNZZDATA1260157511=1547156080-1569380883-null%7C1569398977",
        "pragma": "no-cache",
       # "referer": "https://s.gxrc.com/lz/sjob?page=6",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    #解析详情页中的数据
    def parse_detail(self,response):
        #response.meta返回接收到的meta字典
        item = response.meta['item']
        item['contact_name'] = response.xpath('//*[@id="address"]/table/tbody/tr[2]/td/text()').extract_first().replace(" ", "").replace('\n', '').replace('\r', '')
        item['phone'] =response.xpath('//*[@id="address"]/table/tbody/tr[3]/td/img/@src').extract_first().replace(" ", "").replace('\n', '').replace('\r', '')
        item['e_mail'] =response.xpath('//*[@id="address"]/table/tbody/tr[6]/td/text()').extract_first().replace(" ", "").replace('\n', '').replace('\r', '')
        item['address'] =response.xpath('//*[@id="address"]/table/tbody/tr[1]/td/text()').extract_first().replace(" ", "").replace('\n', '').replace('\r', '')
        yield item
        #总结：两个地方会用到item
        #第一用yield 返回item
        #第二用yield手动发起Requets请求或者是FormRequests请求

    # 填写爬取地址
    start_urls = ['https://s.gxrc.com/lz/sjob?page=439']
    # 编写爬取方法


    def parse(self, response):
        # 实例一个容器保存爬取的信息
        res=response.xpath('//*[@id="posList"]/div')
        index =0
        for box in res:
            index=index+1
            item = LzgxrcUrlitme()
            item['posName'] = box.xpath('.//ul[1]/li[1]/h3/a/text()').extract()[0].strip() #职位
            item['company'] =box.xpath('.//ul[1]/li[2]/a/text()').extract()[0]              #公司名称
            detail_url=box.xpath('.//ul[1]/li[2]/a/@href').extract()[0]                    #详情url
            item['url']=detail_url
            #detail_url=detail_url+'&index='+str(index)
            salary=box.xpath('.//ul[1]/li[3]/text()').extract()                    #薪资
            if len(salary)!=0:
                item['salary']=salary[0]
            else:
                item['salary']=''
            item['workplace']=box.xpath('.//ul[1]/li[4]/text()').extract()[0]               #工作地
            item['updateTime']=box.xpath('.//ul[1]/li[5]/text()').extract()[0]               #更新时间

            item['num']=box.xpath('.//ul[2]/li[1]/span/text()').extract()[0]               #人数
            edu=box.xpath('.//ul[2]/li[2]/span/text()').extract()
            if(len(edu)!= 0):
                item['education']=edu[0]
            else:
                item['education']='不限'
           # item['education']=box.xpath('.//ul[2]/li[2]/span/text()').extract()[0]               #学历
            item['experience']=box.xpath('.//ul[2]/li[3]/span/text()').extract()[0]               #经验
            item['companyType']=box.xpath('.//ul[2]/li[4]/span/text()').extract()[0]               #公司性质
            time.sleep(2)
            #yield item
            #print("detail_url："+detail_url)
            yield FormRequest(url=detail_url,callback=self.parse_detail,meta={'item':item},dont_filter=True)
        #获取下一页的url信息
        nextUrl = response.xpath('//*[@id="Pagination"]/div/ul/li/a/@href').extract()
        if len(nextUrl)!=0 :
            #将信息组合成下一页的url
            page = 'https://s.gxrc.com' + nextUrl[-1]
            #返回url
            yield scrapy.Request(url=page, callback=self.parse)
        #url跟进结束
