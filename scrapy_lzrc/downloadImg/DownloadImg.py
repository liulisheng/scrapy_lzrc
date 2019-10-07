# -*- coding:utf8 -*-
import time
import urllib.request
from urllib.request import urlretrieve
import os
from PIL import Image
import pytesseract
from scrapy_lzrc.MysqlConcetion import MysqlConcetion

def download_img(img_url):

    header ={
        "authority": "s.gxrc.com",
        "method": "GET",
        "path": "/WebPage/AjaxLogin.aspx?showSata=1&randon=0.8016450752555082",
        "scheme": "https",
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
        "x-requested-with": "XMLHttpRequest"
    }
    request = urllib.request.Request(img_url, headers=header)
    strStr=img_url.split('/')
    print('../scrapy_lzrc/img/'+"%s.png"%strStr[-1])
    filename='../img/'+"%s.png"%strStr[-1]
    if os.path.exists(filename):
        print('存在文件：'+filename)
        return filename
    try:
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            print('下载图片')
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filename
    except Exception as e:
        print(e)
        return ''





if __name__ == '__main__':

    while True:
        time.sleep(0.5)
        mysql=MysqlConcetion()
        sql='select id,phone from tb_gxrc_zp_result where phone like "%vip.gxrc.com%" limit 1 '
        result=mysql.select(sql)
        print(result)
        # 下载要的图片
        img_url = result[1]
        filename=download_img(img_url)
        phone=pytesseract.image_to_string(Image.open(filename))
        print('phone：'+phone)
        sql='UPDATE tb_gxrc_zp_result set phone="'+str(phone).replace('"'," ")+'"  where phone="'+str(result[1])+'"'
        print(sql)
        mysql.update(sql)