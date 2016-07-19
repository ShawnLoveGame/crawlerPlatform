#!/usr/bin/python
#coding=utf-8
#author@alingse

import json
import sys

def dec_header(lines):
    headers = {}

    for line in lines.split('\n'):
        line = line.strip()
        if line == "" or not ':' in line:
            continue
        key,value = line[1:].split(':',1)
        key = line[0]+key
        headers[key.strip()] = value.strip()
    return headers
    
if __name__ == '__main__':
    fname = 'requests.header'
    lines = '''
        Host: e.boc.cn
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
        Accept-Encoding: gzip, deflate
        Referer: https://e.boc.cn/ehome/property/floorInfo/toAdd.do
        Connection: keep-alive
        '''
    if len(sys.argv)== 2:
        fname = sys.argv[1]

    if fname != '-t':
        lines = open(fname,'r').read()

    headers = dec_header(lines)
    print(json.dumps(headers,indent=1))