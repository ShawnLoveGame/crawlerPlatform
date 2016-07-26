#coding=utf-8
#author@shibin
#2016.07.26

import requests
import json
import sys

url = 'http://www.cdcredit.gov.cn/EPBaseInfo/getEpBaseInfo.do'

headers = {
    "Origin": "http://www.cdcredit.gov.cn", 
    "Content-Length": "74", 
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6", 
    "Proxy-Connection": "keep-alive", 
    "Accept": "application/json, text/plain, */*", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36", 
    "Host": "www.cdcredit.gov.cn", 
    "Referer": "http://www.cdcredit.gov.cn/www/index.html", 
    "Pragma": "no-cache", 
    "Cache-Control": "no-cache", 
    "Cookie": "sangfor=68437105; yoursessionname1=BC86DCD23C61A70A5D7F57956A389BB4-n1", 
    "content-type": "application/x-www-form-urlencoded", 
    "Accept-Encoding": "gzip, deflate"
}

'''
id=169286949
&unit=1
&unitType=3
&code=
&accpNo=20150612
&regNo=510100000012273
'''
def get_info(data):
    _data = {
        'id':data['id'],
        'unit':1,
        'unitType':3,
        'accpNo':data['accpNo'],
        'regNo':data['regNo']
    }
    try:
        r = requests.post(url,data=_data,headers=headers,timeout=3)
        return r.json()
    except Exception as e:
        pass
        print(e)

