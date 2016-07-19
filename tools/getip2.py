#! /usr/bin/env python
#coding=utf-8

import requests
import sys
import re


def get_ip_tencent():
    url = 'http://vv.video.qq.com/checktime?ran=0.23244502115994692'
    try:
        r = requests.get(url,timeout = 1)
        content = r.content.strip().decode('utf-8')
        sk = content.find('<ip>')
        ek = content.find('</ip>')
        ip = content[sk+4:ek]

        sk = content.find('<pos>')
        ek = content.find('</pos>')
        pos = content[sk+5:ek]
        return ip,pos
    except Exception as e:
        pass
    return ''

if __name__ == "__main__":
    ip,pos = get_ip_tencent()
    print(ip),
    print(pos.encode('utf-8'))
