#coding=utf-8
#author@shibin
#2016.06.28


import requests
from pyquery import PyQuery as pq
from urllib import quote
import time
import json
import sys
import re


url = 'http://app1.sfda.gov.cn/datasearch/face3/search.jsp'

max_pagef = re.compile(u'共(\d+)页').findall
idf = re.compile('&Id=(\d+)').findall

def decode_html(html):
    htmld = pq(html)
    table = htmld('table').eq(2)
    #print table.html().encode('utf-8')
    trs = table('tr')
    item_list = []
    print len(trs)
    for i in range(0,len(trs),2):
        tr = trs.eq(i)
        item = {}
        href = tr('a').attr('href')
        item['id'] = idf(href)[0] 
        item['name'] = tr.text()
        item_list.append(item)
    max_page = int(max_pagef(html)[0])

    return (item_list,max_page)


def searchpage(key = u'壳聚糖',page = 1,**kwargs):
    data = {}
    data['bcId'] = 'null'
    data['State'] = 1
    data['tableId'] = 26
    data['keyword'] = quote(key.encode('utf-8'))
    data['curstart'] = page
    data.update(kwargs)
    try:
        r = requests.post(url,data=data,timeout = 3)
        if r.status_code != 200:
            return False
        html = r.content.decode('utf-8')
        return html
    except Exception as e:
        pass

if __name__ == '__main__':
    
    if len(sys.argv) <= 2:
        key = u'壳聚糖'
        if len(sys.argv) == 2:
            key = sys.argv[1].decode('utf-8')
        page = 1
        html = searchpage(key=key, page=page)
        if html != None and html != False:            
            result = decode_html(html)
            item_list,max_page = result
            print(len(item_list),max_page)
            print(item_list[0])
        exit()
    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    for line in fin:
        key = line.strip().decode('utf-8')
        page = 1
        while True:
            html = searchpage(key=key, page=page)
            if html == None:
                continue
            elif html == False:
                time.sleep(3)
                continue
            else:
                item_list,max_page = decode_html(html)
                print(key,len(item_list),page,max_page)
                for item in item_list:
                    fout.write(json.dumps(item,ensure_ascii=False).encode('utf-8'))
                    fout.write('\n')
                if page >= max_page:
                    break
                page += 1



