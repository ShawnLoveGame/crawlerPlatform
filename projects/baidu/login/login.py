#coding=utf-8
#author@alingse
#2016.06.22

import requests
import commands
import argparse
import time
import os

headers = {
 "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6", 
 "Accept-Encoding": "gzip, deflate, sdch, br", 
 "Host": "m.baidu.com", 
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
 "Upgrade-Insecure-Requests": "1", 
 "Connection": "keep-alive", 
 "Pragma": "no-cache", 
 "Cache-Control": "no-cache", 
 "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
}



def load_cookies(cookief = 'last.cookies'):
    try:
        cookies = json.loads(open(cookief).read())
    except Exception as e:
        pass
    return {}


def dump_cookies(cookies,cookief='last.cookies'):
    try:
        out = json.dumps(cookies,indent=3)
        open(cookief,'w').write(out)
        return True
    except Exception as e:
        pass
    return False


#from http://wappass.baidu.com/static/touch/js/login_8c63308a.js
#2016.06.17 版本
public_key = 'B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F'

'''
#python 加密版本 但是加密不对
#pyrsa
import rsa
import binascii
rsa_key = rsa.PublicKey(int(public_key, 16), 65537)
def py_encrypt(string):
    _pwd = rsa.encrypt(string,rsa_key)
    return binascii.b2a_hex(_pwd)

'''

basepath = os.path.abspath(os.path.dirname(__file__))
def js_encrypt(string,jshell='node'):
    basejs = open('base.js','r').read()
    encjs = '''
        var public_key = "{public_key}";
        var password = "{password}";
        var p = new RSAKeyPair("10001", "",public_key);
        _pwd = encryptedString(p,password);
        
    '''.format(public_key=public_key, password=string)
    printjs = '''
        //for node
        try {
            console.log(_pwd);
        }
        catch(e){
        }
        //for jsbin spider-monkey
        try{
            print(_pwd);
        }
        catch(e){
        }
        '''

    jspath = '{}/{}'.format(basepath,'login.js')
    with open(jspath,'w') as fout:
        fout.write(basejs)
        fout.write(encjs)
        fout.write(printjs)

    _pwd = commands.getoutput(jshell + ' ' +jspath)
    with open(jspath,'w') as fout:
        pass

    return _pwd


home_url = 'https://www.baidu.com/'

passport_url = 'http://wappass.baidu.com/passport/?login&tpl=wimn&ssid%3D0%26amp%3Bfrom%3D%26amp%3Buid%3D%26amp%3Bpu%3Dsz%25401320_1001%252Cta%2540iphone_2_5.0_3_537%26amp%3Bbd_page_type%3D1&tn=&regtype=1&u=http://cp01-mi-wise32.cp01.baidu.com:8080/'


def visit_url(session,url):
    try:
        r = session.get(url,headers=headers,timeout = 2)
        return r.content
    except Exception as e:
        pass


now = lambda :int(time.time()*1000)


def get_servertime(session):
    url = 'http://wappass.baidu.com/wp/api/security/antireplaytoken'
    params = {
        'tpl':'wimn',
        'v':now()
    }
    try:
        r = session.get(url,params = params,headers=headers,timeout = 1)
        return r.json()
    except Exception as e:
        pass


def get_login(session,servertime,username,_pwd):
    url = 'https://wappass.baidu.com/wp/api/login?tt='+str(now())
    uid = session.cookies.get_dict().get('BAIDU_WISE_UID')
    if uid == None:
        uid = str(now())+'_530'

    data = {
            "tpl": "wimn", 
            "uid": uid, 
            "clientfrom": "", 
            "servertime": servertime, 
            "verifycode": "", 
            "login_share_strategy": "", 
            "connect": "0", 
            "skin": "default_v2", 
            "mobilenum": "undefined", 
            "from": "844c", 
            "ssid": "", 
            "bindToSmsLogin": "", 
            "pu": "sz%401320_2001%2Cta%40iphone_1_4.0_3_532", 
            "regist_mode": "", 
            "tn": "", 
            #"gid": "EFD8DD8-3548-4176-8C0D-62CF3D71EFD9", 
            "subpro": "", 
            "regtype": "", 
            "type": "", 
            "username": username, 
            "logLoginType": "wap_loginTouch", 
            "password": _pwd, 
            "countrycode": "", 
            "adapter": "0", 
            "bd_page_type": "1", 
            "loginmerge": "1", 
            "client": "", 
            "action": "login", 
            "vcodestr": "", 
            "isphone": "0"
        }
    try:
        r = session.post(url,data=data,headers=headers,timeout=3)
        jdoc = r.json()
        return jdoc
    except Exception as e:
        pass  


def baidu_login(session,username,password,jshell='node'):
    #prepare
    cookief = 'last.{}.cookies'.format(username)
    lastcookies = load_cookies(cookief)
    for k,v in lastcookies.items():
        session.set(k,v)
    visit_url(session,home_url)
    visit_url(session,passport_url)

    #get servertime
    jdoc = get_servertime(session)
    if jdoc == None:
        return False
    servertime = jdoc['time']

    #encrypt
    pwd = password + servertime
    _pwd = js_encrypt(pwd.encode('utf-8'),jshell=jshell)

    #logins
    jdoc = get_login(session,servertime,username,_pwd)
    if jdoc == None:
        return False
    if jdoc['errInfo']['no'] != '400408':
        return False

    #visit
    goto_url = jdoc['data']['gotoUrl']
    visit_url(session,goto_url)
    content = visit_url(session,home_url)
    print(content)

    dump_cookies(session.cookies.get_dict(),cookief=cookief)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='login username')
    parser.add_argument('password', help='login password')
    parser.add_argument('-j','--jshell',default = 'node', help='js binary to run the jscode') 
    args = parser.parse_args()

    username = args.username
    password = args.password
    jshell = args.jshell

    session = requests.Session()

    status = baidu_login(session,username,password,jshell = jshell)
    print(status)
