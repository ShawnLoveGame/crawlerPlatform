#!/usr/bin/python
#coding=utf-8
#author@shibin

import json
import sys

def dec_cookie(cookie_str):
    cookies = {}
    for line in cookie_str.split(';'):
        line = line.strip()
        if line == "":
            continue
        key,value = line.split('=',1)
        cookies[key.strip()] = value.strip()
    return cookies

if __name__ == '__main__':
    fname = 'requests.cookies'
    lines = '''wbilang_10000=zh_CN;skey=@cOC3Yo1Rs;
        p_skey=-EVv0ccze1UhmBPy2WUt1zY7tVxux1O4af7rGeeqY5A_; 
        pt4_token=Dk6Juu5EnD8fWOce9SMpWOfL*vUkfdmuJ4H-qxvWz1A_; 
        wb_regf=%3B0%3B%3Bmessage.t.qq.com%3B0; 
        pgv_info=ssid=s49775644;ts_last=t.qq.com/augming;ts_refer=e.t.qq.com/mobile_pandora;
        pgv_pvid=5364005095'''
    if len(sys.argv)== 2:
        fname = sys.argv[1]

    if fname != '-t':
        lines = open(fname,'r').read()

    cookies = dec_cookie(lines)
    print(json.dumps(cookies,indent=1))


