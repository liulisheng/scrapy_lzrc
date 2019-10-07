# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.response import response_status_message

from scrapy_lzrc.settings import UAPOOL
from scrapy_lzrc.MysqlConcetion import MysqlConcetion

class ScrapyLzrcSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyLzrcDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        #return response
        if response.status != 200:
            print('状态码异常')
            reason = response_status_message(response.status)
            time.sleep(random.randint(10,20))
            print("测试响应")
            return self._retry(request,reason,spider)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
# IP代理池
class IPPOOLS(HttpProxyMiddleware):
    def __init__(self, ip=""):
        self.ip = ip

    def process_request(self, request, spider):

        try:
            con= MysqlConcetion()
            result=con.select( """SELECT ip,port FROM `tb_ippools` where status=0   ORDER BY  RAND() LIMIT 0,1 """)
            print("当前使用的IP为： " + result[0]+":"+str(result[1]))
            request.meta["proxy"] = "http://" + result[0]+":"+str(result[1])
        except Exception as e:
            print(e)
            pass
    def process_exception(self, request, exception, spider):
        if exception:
            try:
                proxy = request.meta["proxy"].split("/")[-1]
                print("删除失效IP"+proxy)
                proxyArray=proxy.split(':')
                con= MysqlConcetion()
                sql = "UPDATE tb_ippools SET status =1 WHERE ip = '"+proxyArray[0]+ "'  and port="+str(proxyArray[1])
                con.update(sql)
            except Exception as e:
                print(e)
                pass
            return request



# 用户代理池
class Uamid(UserAgentMiddleware):
    def __init__(self, user_agent=""):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        print("当前使用的User-Agent是： " + thisua)
        request.headers.setdefault("User-Agent", thisua)
    def process_exception(self, request, exception, spider):

        if exception:
            try:
                proxy = request.meta["proxy"].split("/")[-1]
                print("删除失效IP"+proxy)
                proxyArray=proxy.split(':')
                con= MysqlConcetion()
                sql = "UPDATE tb_ippools SET status =1 WHERE ip = '"+proxyArray[0]+ "'  and port="+str(proxyArray[1])
                con.update(sql)
            except Exception as e:
                print(e)
                pass
            return request


