#coding=utf-8
#2016.07.15

import requests
import json
import time
import sys

import requests.packages.urllib3.util.ssl_
#print(requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

now = lambda: int(1000*time.time())

def get_detail(item_id = '525528798012'):
    url = 'https://mdskip.taobao.com/core/initItemDetail.htm'
    params = {
        "household": "false", 
        "isRegionLevel": "false", 
        "offlineShop": "false", 
        "queryMemberRight": "true", 
        "isUseInventoryCenter": "false", 
        "isApparel": "false", 
        "isSecKill": "true", 
        "cachedTimestamp": now(), 
        "isAreaSell": "false", 
        "isForbidBuyItem": "false", 
        "sellerPreview": "false", 
        "isPurchaseMallPage": "false", 
        "cartEnable": "true", 
        "timestamp": now(), 
        "tryBeforeBuy": "false", 
        "showShopProm": "false", 
        "tmallBuySupport": "true", 
        "addressLevel": "3", 
        "itemId": item_id, 
        "callback": "setMdskip", 
        "service3C": "false", 
        #"isg": "An19DNx-2se7Vz3t4Ez-DKWWDcJ3FLFs"
    }

    headers = {
        "accept-language": "zh-CN,zh;q=0.8,en;q=0.6", 
        "accept-encoding": "gzip, deflate, sdch, br", 
        "accept": "*/*", 
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36", 
        "cookie": "v=0; cookie2=1c49d1dc6d737d1a8b6634834559b408; t=ad5d4bfe7e49d8a230e9ce8f4da70b7c; cna=vttLEARrqxsCAbaUQzOSYVab; thw=cn; _tb_token_=e5eb36e615eeb; uc1=cookie14=UoWwJr6kOgb0TQ%3D%3D; isg=AldXelRzzGuB40jmdAvmuP9K5s0WHCv-RpgHPamEcyaN2HcasWy7ThX6TM-8; mt=ci%3D-1_0; l=Al5e5tyWo3ZiYcWFkBgtVLjDLv6gJiOq", 
        "pragma": "no-cache", 
        "cache-control": "no-cache", 
        "referer": "https://detail.tmall.com/item.htm?spm=a230r.1.14.89.xohYSn&id={}&ns=1&abbucket=1".format(item_id)
    }
    #这里是请求数据的
    try:
        #params query数据，headers，request 头数据
        r = requests.get(url,params=params, headers=headers, timeout=2)
        text = r.content.strip().decode('gbk','ignore')
        return text
    except Exception as e:
        print e
        pass

def get_start(text):
    sk = text.find('{')
    ek = text.rfind('}')
    jcontent = text[sk:ek+1]
    #print(jcontent.encode('utf-8'))
    try:
        jdoc = json.loads(jcontent)
        start = jdoc['defaultModel']['tradeResult']['startTime']
    except Exception as e:
        print(e,jcontent)
        return False
    return start



if __name__ == '__main__':
    item_id = '525528798012'
    if len(sys.argv) == 2:
        item_id = sys.argv[1]
    text = get_detail(item_id = item_id)
    if text == None:
        exit()
    start = get_start(text)
    x = time.localtime(start*1.0/1000)
    print item_id,time.strftime('%Y-%m-%d %H:%M:%S',x)






