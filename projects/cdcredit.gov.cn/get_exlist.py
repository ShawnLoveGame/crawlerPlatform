#coding=utf-8

import requests
import json
import time
import sys

url = 'http://www.cdcredit.gov.cn/service/exceptionList'

headers = {
    "Origin": "http://www.cdcredit.gov.cn", 
    "Content-Length": "34", 
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6", 
    "Proxy-Connection": "keep-alive", 
    "Accept": "application/json, text/plain, */*", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36", 
    "Host": "www.cdcredit.gov.cn", 
    "Referer": "http://www.cdcredit.gov.cn/www/index.html", 
    "Pragma": "no-cache", 
    "Cache-Control": "no-cache", 
    #"Cookie": "sangfor=68437105; yoursessionname1=BC86DCD23C61A70A5D7F57956A389BB4-n1", 
    "content-type": "application/x-www-form-urlencoded", 
    "Accept-Encoding": "gzip, deflate"
}

def get_page(page,page_size = 20):
    data = {
        'page':page,
        'pageSize':page_size,
        'appType':'APP001'
    }
    try:
        r = requests.post(url,data=data,headers=headers,timeout=4)
        return r.json()
    except Exception as e:
        pass
        print(e)


def main(fout):
    page = 1
    pages = list(range(993,1923))
    while pages != []:
        page = pages.pop(0)
        jdoc = get_page(page)
        if jdoc == None:
            print(page,None)
            pages.append(page)
        else:
            jdoc['_page'] = page
            fout.write(json.dumps(jdoc,ensure_ascii=False).encode('utf-8'))
            fout.write('\n')

if __name__ == '__main__':
    fout = open(sys.argv[1],'w')
    main(fout)
