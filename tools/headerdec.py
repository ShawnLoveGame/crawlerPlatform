#!/usr/bin/python
#coding=utf-8
#author@shibin

import sys
import json
def dec_header(header_str):
    headers={}
    for line in header_str.split('\n'):
        line=line.strip()
        if line=="" or not ':' in line:
            continue
        header,value=line[1:].split(':',1)
        headers[line[0:1]+header.strip()]=value.strip()
    return headers,json.dumps(headers,indent=1)#,ensure_ascii=False).encode('utf-8')

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=="test":
        test_headerstr='''
Host: e.boc.cn
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://e.boc.cn/ehome/property/floorInfo/toAdd.do
Cookie: DWRSESSIONID=zQMFsW*2YbkjZqIjW7vQ5PfWQWk; JSESSIONID_eproperty=0000Ps5CG5ItwQlC27cFkuQPrWE:-1
Connection: keep-alive
'''
        _,s=dec_header(test_headerstr)
        print s
        exit()
    if len(sys.argv)==1:
        fname='requests.header'
    else:
        fname=sys.argv[1]
    lines=open(fname,'r').read()
    _,s=dec_header(lines)
    print s




