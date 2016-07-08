#coding=utf-8
#author@shibin
#2016.06.28


import requests
from pyquery import PyQuery as pq
import time
import json
import sys
import re



url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=26&tableName=TABLE26&tableView=%B9%FA%B2%FA%C6%F7%D0%B5&Id=116849'

def get_detail(item_id = 116849,**kwargs):
    url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp'
    params = {}
    params['tableId'] = 26
    params['tableName'] = 'TABLE26'
    params['tableView'] = ''
    params['Id'] = item_id
    params.update(kwargs) 
    
    try:
        r = requests.get(url, params=params,timeout=3)
        if r.status_code != 200:
            return False
        html = r.content.decode('utf-8')
        return html
    except Exception as e:
        pass


def decode_detail_html(html):
    item_info = {}
    htmld = pq(html)
    table = htmld('table')
    trs = table('tr')
    for i in range(1,len(trs)):
        tr = trs.eq(i)
        key = tr('td').eq(0).text()
        value = tr('td').eq(1).text()
        item_info[key] = value

    return item_info



if __name__ == '__main__':
    if len(sys.argv) <= 2:
        item_id = 116849
        if len(sys.argv) == 2:
            item_id = int(sys.argv[1])

        html = get_detail(item_id = item_id)
        if html != None or item_id != False:
            item_info = decode_detail_html(html)
            print(json.dumps(item_info,ensure_ascii=False).encode('utf-8'))
        exit()
    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    for line in fin:
        item_id = int(line.strip())
        while True:
            html = get_detail(item_id=item_id)
            if html == None:
                continue
            elif html == False:
                time.sleep(3)
                continue
            else:                
                item_info = decode_detail_html(html)
                print(item_id,len(item_info.keys()))
                fout.write(json.dumps(item_info,ensure_ascii=False).encode('utf-8'))
                fout.write('\n')
                break












