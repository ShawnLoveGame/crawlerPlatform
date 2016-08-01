#! /usr/bin/env python
#coding=utf-8

import requests
import json
import sys

headers = {
   "Accept-Language": "zh-CN,zh;q=0.8", 
   "Accept-Encoding": "gzip, deflate, sdch", 
   "Accept": "*/*", 
   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36", 
   "Host": "fw.qq.com", 
   "Referer": "http://ilike.qq.com/", 
   "Proxy-Connection": "keep-alive"
}

def get_ip_tencent():
    url = 'http://fw.qq.com/ipaddress?random=0.31905940761720486'
    try:
        r = requests.get(url,headers = headers,timeout = 1)
        content = r.content.strip().decode('gbk')
        sk = content.find('(')
        ek = content.rfind(')')
        content = content[sk+1:ek]
        return content
    except Exception as e:
        pass
    return ''

if __name__ == "__main__":
    content = get_ip_tencent()
    print(content)
