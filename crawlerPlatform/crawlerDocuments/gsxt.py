# -*-: coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError, RequestException
import json
import math
import datetime
import pymysql
import time
from pybloom_live import BloomFilter, ScalableBloomFilter
import traceback
from SetProxy import Ss
from retrying import retry


class GSXT:
    def __init__(self, searchword):
        self.base_url = 'http://app.gsxt.gov.cn/'
        self.search_url = 'http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1'
        self.detail_url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-primaryinfoapp-entbaseInfo-{}.html?nodeNum={}&entType={}'
        self.headers = {
            'Host': 'app.gsxt.gov.cn',
            'Connection': 'keep-alive',
            'Content-Length': '2',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'file://',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; VKY-AL00 Build/HUAWEIVKY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 Html5Plus/1.0',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Cookie': '__jsluid=c4b165b7c3aed96d6a6da49b76cbeb94;JSESSIONID=E22B1C6516882041B052A576092875CA;SECTOKEN=7146152019179079477;tlb_cookie=172.16.12.1048080'
        }
        self.searchword = searchword
        self.host = '192.168.1.68'
        self.port = '3306'
        self.user = 'root'
        self.passwd = '123456'
        self.database = 'phtest'
        self.ss = Ss()
        self.proxy = {}

    def get_search_page(self, url):
        form_data = {
            "searchword": self.searchword.encode("utf-8").decode("latin1"),
            "conditions": json.loads(
                '{"excep_tab": "0","ill_tab": "0","area": "0","cStatus": "0","xzxk": "0","xzcf": "0","dydj": "0"}'),
            "sourceType": "A"
        }
        try:
            response1 = requests.post(url, headers=self.headers, proxies=self.proxy,timeout=6,
                                      data=json.dumps(form_data, ensure_ascii=False))
            response1.encoding = "gbk"
            print(response1.text)
            print(response1.status_code)
        except Exception as e:
            print(e)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_search_page(url)

        try:
            data = json.loads(response1.text)
            status = int(data['status'])
            # print(data)
            # status = data['status']
            if response1.status_code == 200 and data['data'] and status != 500:
                return response1.text
        except Exception as e:
            print(e)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_search_page(url)

    def get_detail_page(self, pripid, nodeNum, entType):

        detailurl = self.detail_url.format(pripid, nodeNum, entType)
        print(detailurl)
        try:
            response2 = requests.post(url=detailurl, headers=self.headers,timeout=6, proxies=self.proxy, json={})
        except Exception as e:
            print(e)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_detail_page(pripid, nodeNum, entType)

        try:
            data = json.loads(response2.text)
            print(response2.status_code)
            print(data)
            if response2.status_code == 200:
                return response2.text
        except:
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_detail_page(pripid, nodeNum, entType)
        if 'status' in data:
            status = int(data['status'])
            if status == 500:
                self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
                self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
                self.get_PROXY()
                return Exception

    def get_json_data(self, url):
        try:
            response = requests.post(url, headers=self.headers,timeout=6, proxies=self.proxy, json={})
            print(response.text)
            response.encoding = 'utf-8'
            print(response.status_code)
        except Exception as e:
            print(e)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_json_data(url)
        try:
            json_data = json.loads(response.text)
            if response.status_code == 200 and json_data is not None:
                while 'NGIDERRORCODE' not in json_data:
                    print(json_data)
                    return json_data
                else:
                    self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
                    self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
                    self.get_PROXY()
                    print(json_data)
                    return self.get_json_data(url)
            if 'status' in json_data:
                status = int(json_data['status'])
                if status == 500:
                    self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
                    self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
                    self.get_PROXY()
                    return self.get_json_data(url)
                return None
            return None
        except Exception as e:
            print(e)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
            self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
            self.get_PROXY()
            return self.get_json_data(url)

    # 解析详情页
    def parse_detail_page(self, detail_page):
        bloom_sql = "select entName, uniscId,register_num, person_name, estDate, dom, entType, regState, opFrom, opTo, apprDate, regOrg, opScope, statusDate,cancel_reason,regCap,regCaption,regCapCurCN from gsxt"
        base_b = self.get_bloomFilter(bloom_sql)
        print(detail_page)
        detail_data = json.loads(detail_page)
        print(detail_data)
        # 基本信息
        item = {}
        # 注册资本
        item['regCap'] = self.ExistOrNot(detail_data, "regCap")
        item['regCaption'] = self.ExistOrNot(detail_data, "regCaption")
        if item['regCaption']:
            item['regCaption'] += "万"
        item['regCapCurCN'] = self.ExistOrNot(detail_data, "regCapCurCN")
        if not item['regCapCurCN']:
            item['regCapCurCN'] = "人民币"
        if detail_data['result']:
            # 开始拆分数据

            # 企业名
            # item['entName'] = detail_data['result']['entName']
            item['entName'] = self.ExistOrNot(detail_data['result'], 'entName', 'traName')
            # 统一社会信用代码
            item['uniscId'] = detail_data['result']['uniscId']
            # 工商注册号
            item['register_num'] = detail_data['result']['regNo']
            # 执行事务合伙人或法定代表人
            item['person_name'] = detail_data['result']['name']
            # 成立时间
            item['estDate'] = detail_data['result']['estDate']
            # 地址
            # item['dom'] = detail_data['result']['dom']
            item['dom'] = self.ExistOrNot(detail_data['result'], 'dom', 'opLoc')
            # 类型
            item['entType'] = detail_data['result']['entType_CN']
            # 登记状态
            item['regState'] = detail_data['result']['regState_CN']
            # 合伙期始
            # item['opFrom'] = detail_data['result']['opFrom']
            item['opFrom'] = self.ExistOrNot(detail_data['result'], 'opFrom')
            # 合伙期至
            # item['opTo'] = detail_data['result']['opTo']
            item['opTo'] = self.ExistOrNot(detail_data['result'], 'opTo')
            # 核准日期
            # item['apprDate'] = detail_data['result']['apprDate']
            item['apprDate'] = self.ExistOrNot(detail_data['result'], 'apprDate')
            # 登记机关
            item['regOrg'] = detail_data['result']['regOrg_CN']
            # 经营范围
            item['opScope'] = detail_data['result']['opScope']
            # 状态决定日期
            # item['statusDate'] = detail_data['statusInfo']['statusDate']
            item['statusDate'] = self.ExistOrNot(detail_data['statusInfo'], 'statusDate')
            # 注销原因
            # item['cancel_reason'] = detail_data['statusInfo']['reason']
            item['cancel_reason'] = self.ExistOrNot(detail_data['statusInfo'], 'reason')
        print(item)
        if item in base_b:
            print("已存在数据库")
        else:
            base_b.add(item)
            self.insert_base_data(item)
        return item

    # 插入基本信息
    def insert_base_data(self, item):
        print("插入基本信息")
        uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gsxt(entName,uniscId,register_num,person_name,estDate,dom,entType,regState,opFrom,opTo,apprDate,regOrg,opScope,statusDate,cancel_reason,local_utime,regCap,regCaption,regCapCurCN) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql,
                           (
                               item['entName'], item['uniscId'], item['register_num'], item['person_name'],
                               item['estDate'],
                               item['dom'], item['entType'], item['regState'], item['opFrom'],
                               item['opTo'], item['apprDate'], item['regOrg'], item['opScope'],
                               item['statusDate'], item['cancel_reason'], uptime, item['regCap'], item['regCaption'],
                               item['regCapCurCN']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取股东及出资信息
    def get_holder_detail(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-shareholder-{}.html?nodeNum={}&entType={}&start=0&sourceType=A '
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        print("股东url")
        print(url)
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        index = 0
        for i in range(totalPage):
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-shareholder-{}.html?nodeNum={}&entType={}&start={}&sourceType=A '
            if i is not 0:
                index += 5
            url = url.format(params['pripid'], params['nodeNum'], params['entType'], str(index))
            json_data = self.get_json_data(url)
            print(json_data)
            data = json_data['data']
            if data is not None:
                bsql = 'select inv_name, invType, blicType, bLicNo, respForm from gx_holder'
                b = self.get_bloomFilter(bsql)
                for g in range(len(data)):
                    item = {}
                    # 股东
                    item['inv_name'] = data[g]['inv']
                    # 股东类型
                    item['invType'] = data[g]['invType_CN']
                    # 企业执照类型
                    item['blicType'] = data[g]['blicType_CN']
                    # 注册号
                    item['bLicNo'] = data[g]['bLicNo']
                    # 企业类型
                    item['respForm'] = data[g]['respForm_CN']
                    # 获取下一个url的参数
                    invId = data[g]['invId']
                    print('股东信息')
                    print(item)
                    # 插入股东基本信息
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_holder_base(item, params['main_id'])
                    # 获取详细股东出资信息
                    detail_url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-shareholderDetail-{}.html?entType={}&sourceType=A '.format(
                        invId, params['entType'])
                    print(detail_url)

                    h_data = self.get_json_data(detail_url)
                    print(h_data)
                    main_id = self.get_main_id(item['inv_name'])
                    inv_name = item['inv_name']
                    h_data1 = h_data['data'][1]
                    if h_data1 is not None:
                        bsql = 'select subConAm, conForm, conDate from gx_holder_con'
                        b = self.get_bloomFilter(bsql)
                        for j in range(len(h_data1)):
                            # 认缴出资金额
                            confirm = {}
                            confirm['subConAm'] = h_data1[j]['subConAm']
                            # 认缴出资方式
                            confirm['conForm'] = h_data1[j]['conForm_CN']
                            # 认缴出资时间
                            confirm['conDate'] = h_data1[j]['conDate']
                            print(confirm)
                            # 插入认缴出资表
                            if item in b:
                                print("已存在数据库")
                            else:
                                b.add(item)
                                self.insert_holder_confirm(confirm, main_id, inv_name)
                    h_data0 = h_data['data'][0]
                    if h_data0 is not None:
                        bsql = 'select acConAm, conDate, conForm from gx_holder_rea'
                        b = self.get_bloomFilter(bsql)
                        for j in range(len(h_data0)):
                            realHan = {}
                            # 实缴金额
                            realHan['acConAm'] = h_data0[j]['acConAm']
                            # 日期
                            realHan['conDate'] = h_data0[j]['conDate']
                            # 币种
                            realHan['conForm'] = h_data0[j]['conForm_CN']
                            print(realHan)
                            if item in b:
                                print("已存在数据库")
                            else:
                                b.add(item)
                                self.insert_holder_reahand(realHan, main_id, inv_name)

    # 插入股东及出资信息
    def insert_holder_base(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_holder(c_id, inv_name,invType,blicType,bLicNo,respForm) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['inv_name'], item['invType'], item['blicType'], item['bLicNo'],
                                 item['respForm']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    def insert_holder_confirm(self, confirm, main_id, inv_name):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_holder_con(c_id, inv_name,subConAm,conForm,conDate) values (%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, inv_name, confirm['subConAm'], confirm['conForm'], confirm['conDate']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    def insert_holder_reahand(self, realHan, main_id, inv_name):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_holder_rea(c_id, inv_name,acConAm,conDate,conForm) values (%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, inv_name, realHan['acConAm'], realHan['conDate'], realHan['conForm']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取主要人员信息
    def get_leader(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-KeyPerson-{}.html?nodeNum={}&entType={}&sourceType=A '
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        print('主要人员url')
        print(url)

        json_data = self.get_json_data(url)
        print(json_data)
        data = json_data['data']
        if data is not None:
            bsql = 'select lename, leposition from gx_leader'
            b = self.get_bloomFilter(bsql)
            for i in range(len(data)):
                item = {}
                # 名字
                item['lename'] = data[i]['name']
                # 职位
                item['leposition'] = data[i]['position_CN']
                # 插入主要人员信息
                print(item)
                if item in b:
                    print("已存在数据库")
                else:
                    b.add(item)
                    self.insert_leader(item, params['main_id'])

    # 插入主要人员信息
    def insert_leader(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_leader(c_id, lename,leposition) values (%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['lename'], item['leposition']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取企业变更信息
    def get_entprise_info_after(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-alter-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-alter-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select altItem, altBe, altAf,altDate from gx_change'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 变更事项
                    item['altItem'] = data[j]['altItem_CN']
                    # 变更前
                    item['altBe'] = data[j]['altBe']
                    # 变更后
                    item['altAf'] = data[j]['altAf']
                    # 变更日期
                    item['altDate'] = data[j]['altDate']
                    print("变更信息")
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_change(item, params['main_id'])

    # 插入变更信息
    def insert_change(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_change(c_id, altItem,altBe,altAf,altDate) values (%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['altItem'], item['altBe'], item['altAf'], item['altDate']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取分支机构信息
    def get_branch(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-branch-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])

        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 9
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-branch-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select brName, regNo, regOrg, uniscId from gx_branch'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 名称
                    item['brName'] = data[j]['brName']
                    # 注册号
                    item['regNo'] = data[j]['regNo']
                    # 登记机关
                    item['regOrg'] = data[j]['regOrg_CN']
                    # 社会统一码
                    item['uniscId'] = data[j]['uniscId']
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_branch(item, params['main_id'])
                    print(item)

    # 插入分支机构信息
    def insert_branch(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_branch(c_id, brName,regNo,regOrg,uniscId) values (%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['brName'], item['regNo'], item['regOrg'], item['uniscId']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取动产抵押登记信息
    def get_mortreg(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-mortreginfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])

        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        print('动产登记页数')
        print(totalPage)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-mortreginfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select morRegCNo, regiDate, regOrg, priClaSecAm,publicDate,regCapCur,canDate from gx_mortreg'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 登记编号
                    item['morRegCNo'] = data[j]['morRegCNo']
                    # 注册时间
                    item['regiDate'] = data[j]['regiDate']
                    # 登记机关
                    item['regOrg'] = data[j]['regOrg_CN']
                    # 被担保债权数额
                    item['priClaSecAm'] = data[j]['priClaSecAm']
                    # 公示日期
                    item['publicDate'] = data[j]['publicDate']
                    # 币种
                    item['regCapCur'] = data[j]['regCapCur_Cn']
                    # 注销日期
                    item['canDate'] = data[j]['canDate']
                    print("动产登记")
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_mortreg(item, params['main_id'])

    # 插入动产抵押登记信息
    def insert_mortreg(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_mortreg(c_id, morRegCNo,regiDate,regOrg,priClaSecAm,publicDate,regCapCur,canDate) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['morRegCNo'], item['regiDate'], item['regOrg'], item['priClaSecAm']
                                 , item['publicDate'], item['regCapCur'], item['canDate']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)

    # 获取股权出质登记信息
    def get_stakqualitinfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-stakqualitinfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])

        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        print('股权出质页数')
        print(totalPage)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-stakqualitinfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)
            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select equityNo, equPleDate, pledgor, impAm,impOrg,impOrgBLicType,regCapCur,status,publicDate,canDate,equPleCanRea from gx_staqualit'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 登记编号
                    item['equityNo'] = data[j]['equityNo']
                    # 登记日期
                    item['equPleDate'] = data[j]['equPleDate']
                    # 出质人
                    item['pledgor'] = data[j]['pledgor']
                    # 出质股权数额
                    item['impAm'] = data[j]['impAm']
                    # 质权人
                    item['impOrg'] = data[j]['impOrg']
                    # 质权人类型
                    item['impOrgBLicType'] = data[j]['impOrgBLicType_CN']
                    # 币种
                    item['regCapCur'] = data[j]['regCapCur_CN']
                    # 状态
                    item['status'] = data[j]['type']
                    # 公示日期
                    item['publicDate'] = data[j]['publicDate']
                    # 取消日期
                    item['canDate'] = data[j]['canDate']
                    # 取消原因
                    item['equPleCanRea'] = data[j]['equPleCanRea']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_stakqualit(item, params['main_id'])

    # 插入股权出质登记信息
    def insert_stakqualit(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_staqualit(c_id, equityNo,equPleDate,pledgor,impAm,impOrg,impOrgBLicType,regCapCur,status,publicDate,canDate,equPleCanRea) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['equityNo'], item['equPleDate'], item['pledgor'], item['impAm']
                                 , item['impOrg'], item['impOrgBLicType'], item['regCapCur'], item['status'],
                                 item['publicDate'], item['canDate'], item['equPleCanRea']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取商标注册信息
    def get_trademark(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-trademark-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        print('商标注册信息页数')
        print(totalPage)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-trademark-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)
            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select regNum,intCls,regAnncDate,regAnncIssue,propertyEndDate,propertyBgnDate,goodsCnName from gx_trademark'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 商标注册号
                    item['regNum'] = data[j]['regNum']
                    # 类别
                    item['intCls'] = data[j]['intCls']
                    # 注册公告日期
                    item['regAnncDate'] = data[j]['regAnncDate']
                    # 注册公告期号
                    item['regAnncIssue'] = data[j]['regAnncIssue']
                    # 专用权起始日期
                    item['propertyEndDate'] = data[j]['propertyEndDate']
                    # 专用权终止日期
                    item['propertyBgnDate'] = data[j]['propertyBgnDate']
                    # 商品/服务项目
                    item['goodsCnName'] = data[j]['goodsCnName']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_trademark(item, params['main_id'])

    # 插入商标注册信息
    def insert_trademark(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_trademark(c_id, regNum,intCls,regAnncDate,regAnncIssue,propertyEndDate,propertyBgnDate,goodsCnName) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['regNum'], item['intCls'], item['regAnncDate'], item['regAnncIssue']
                                 , item['propertyEndDate'], item['propertyBgnDate'], item['goodsCnName']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取司法协助信息
    def get_assistInfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/Affiche-query-info-assistInfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('司法协助信息条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/Affiche-query-info-assistInfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select publicDate,inv,froAm,frozState_CN,executeNo,bLicType_CN,bLicNo,cerNo from gx_assist_info'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 公示时间
                    item['publicDate'] = data[j]['publicDate']
                    # 被执行人
                    item['inv'] = data[j]['inv']
                    # 股权数额
                    item['froAm'] = data[j]['froAm']
                    # 股权状态
                    item['frozState_CN'] = data[j]['frozState_CN']
                    # 执行通知书文号
                    item['executeNo'] = data[j]['executeNo']
                    # 被执行人证照种类
                    item['bLicType_CN'] = data[j]['bLicType_CN']
                    # 被执行人证照号码
                    item['bLicNo'] = data[j]['bLicNo']
                    # 执行裁定文书号
                    item['cerNo'] = data[j]['cerNo']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_assistInfo(item, params['main_id'])

    # 插入司法协助信息
    def insert_assistInfo(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_assist_info(c_id, publicDate,inv,froAm,frozState_CN,executeNo,bLicType_CN,bLicNo,cerNo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['publicDate'], item['inv'], item['froAm'], item['frozState_CN'],
                item['executeNo'], item['bLicType_CN'], item['bLicNo'], item['cerNo']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取行政许可信息
    def get_licenceinfoDetail(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-licenceinfoDetail-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('行政许可信息条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-licenceinfoDetail-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select licNo,licName_CN,licAnth,valFrom,valTo,licItem from gx_licenceinfodetail'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 许可文件编号
                    item['licNo'] = data[j]['licNo']
                    # 许可文件名称
                    item['licName_CN'] = data[j]['licName_CN']
                    # 许可机关
                    item['licAnth'] = data[j]['licAnth']
                    # 有效起始时间
                    item['valFrom'] = data[j]['valFrom']
                    # 有效终止时间
                    item['valTo'] = data[j]['valTo']
                    # 许可内容
                    item['licItem'] = data[j]['licItem']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_licenceinfoDetail(item, params['main_id'])

    # 插入行政许可信息
    def insert_licenceinfoDetail(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_licenceinfodetail(c_id, licNo,licName_CN,licAnth,valFrom,valTo,licItem) values (%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['licNo'], item['licName_CN'], item['licAnth'], item['valFrom']
                                 , item['valTo'], item['licItem']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取行政处罚信息
    def get_punishmentdetail(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-punishmentdetail-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('行政处罚信息条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-punishmentdetail-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select penDecNo,illegActType,penContent,penAuth_CN,penDecIssDate from gx_punishmentdetail'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 决定书文号
                    item['penDecNo'] = data[j]['penDecNo']
                    # 违法行为类型
                    item['illegActType'] = data[j]['illegActType']
                    # 行政处罚内容
                    item['penContent'] = data[j]['penContent']
                    # 决定机关名称
                    item['penAuth_CN'] = data[j]['penAuth_CN']
                    # 处罚决定日期
                    item['penDecIssDate'] = data[j]['penDecIssDate']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_punishmentdetail(item, params['main_id'])

    # 插入行政处罚信息
    def insert_punishmentdetail(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_punishmentdetail(c_id, penDecNo,illegActType,penContent,penAuth_CN,penDecIssDate) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['penDecNo'], item['illegActType'], item['penContent'], item['penAuth_CN']
                                 , item['penDecIssDate']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取抽查检查结果信息
    def get_spotCheckInfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-spotCheckInfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('抽查检查结果信息条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-spotCheckInfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select insAuth_CN,insDate,insRes_CN from gx_spotcheckinfo'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 检查实施机关
                    item['insAuth_CN'] = data[j]['insAuth_CN']
                    # 日期
                    item['insDate'] = data[j]['insDate']
                    # 结果
                    item['insRes_CN'] = data[j]['insRes_CN']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_spotCheckInfo(item, params['main_id'])

    # 插入抽查检查结果信息
    def insert_spotCheckInfo(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_spotcheckinfo(c_id, insAuth_CN,insDate,insRes_CN) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['insAuth_CN'], item['insDate'], item['insRes_CN']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 列入严重违法失信企业名单（黑名单）信息
    def get_illInfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-illInfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('黑名单条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-illInfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select abntime,serILLRea_CN,decOrg_CN from gx_illinfo'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 列入日期
                    item['abntime'] = data[j]['abntime']
                    # 列入原因
                    item['serILLRea_CN'] = data[j]['serILLRea_CN']
                    # 作出决定机关（列出）
                    item['decOrg_CN'] = data[j]['decOrg_CN']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_illInfo(item, params['main_id'])

    # 插入黑名单信息
    def insert_illInfo(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_illinfo(c_id, abntime,serILLRea_CN,decOrg_CN) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['abntime'], item['serILLRea_CN'], item['decOrg_CN']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 列入经营异常信息
    def get_entBusExcep(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-entBusExcep-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('经营异常条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-entBusExcep-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select abntime,speCause_CN,decOrg_CN from gx_entbusexcep'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 列入日期
                    item['abntime'] = data[j]['abntime']
                    # 列入原因
                    item['speCause_CN'] = data[j]['speCause_CN']
                    # 作出决定机关（列出）
                    item['decOrg_CN'] = data[j]['decOrg_CN']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_entBusExcep(item, params['main_id'])

    # 插入经营异常信息
    def insert_entBusExcep(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_entbusexcep(c_id, abntime,speCause_CN,decOrg_CN) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id, item['abntime'], item['speCause_CN'], item['decOrg_CN']
                                 ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取企业年报信息
    def get_annualReportInfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-anCheYearInfo-{}.html?nodeNum={}&entType={}&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        for i in range(len(json_data)):
            anCheId = json_data[i]['anCheId']
            anCheYear = json_data[i]['anCheYear']
            anCheDate = json_data[i]['anCheDate']
            print(anCheYear, "年度报告", " 时间：", anCheDate)
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-primaryinfoapp-annualReportInfo-{}.html?nodeNum={}&anCheId={}&anCheYear={}&entType={}&sourceType=A'
            url = url.format(params['pripid'], params['nodeNum'], anCheId, anCheYear, params['entType'])

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['annRep']
            print(type(data))
            annRepData = {}
            # 基本信息
            annRepData['tel'] = data['annRepData']['tel']
            if 'email' in data['annRepData'].keys():
                annRepData['email'] = data['annRepData']['email']
            else:
                annRepData['email'] = 'xxx'
            print(annRepData)
            self.insert_annRepData(annRepData, params['main_id'], anCheYear)
            # 对外投资信息
            if 'annRepDataInvestment' in data.keys():
                annRepDataInvestment = data['annRepDataInvestment']
                # RepDataInvestment = annRepDataInvestment['entName']
                for i in range(len(annRepDataInvestment)):
                    investment = {}
                    # 对外投资公司名称
                    investment['entName'] = annRepDataInvestment[i]['entName']
                    # 对外投资公司统一社会信用代码
                    investment['uniscId'] = annRepDataInvestment[i]['uniscId']
                    print(investment)
                    self.insert_annRepDataInvestment(investment, params['main_id'], anCheYear)
            # 网站或网店信息
            if 'annRepDataWebsite' in data.keys():
                annRepDataWebsite = data['annRepDataWebsite']
                for i in range(len(annRepDataWebsite)):
                    Website = {}
                    # 网站名称
                    Website['webSitName'] = annRepDataWebsite[i]['webSitName']
                    # 网址
                    Website['domain'] = annRepDataWebsite[i]['domain']
                    print(Website)
                    self.insert_annRepDataWebsite(Website, params['main_id'], anCheYear)
            # 股东及出资信息
            if 'annRepDataSponsor' in data.keys():
                annRepDataSponsor = data['annRepDataSponsor']
                for i in range(len(annRepDataSponsor)):
                    sponsor = {}
                    # 出资人名称
                    sponsor['invName'] = annRepDataSponsor[i]['invName']
                    # 认缴出资额（万元）
                    sponsor['liSubConAm'] = annRepDataSponsor[i]['liSubConAm']
                    # 认缴出资时间
                    sponsor['subConDate'] = annRepDataSponsor[i]['subConDate']
                    # 认缴出资方式
                    sponsor['subConFormName'] = annRepDataSponsor[i]['subConFormName']
                    # 实缴出资额（万元）
                    sponsor['liAcConAm'] = annRepDataSponsor[i]['liAcConAm']
                    # 实缴出资时间
                    sponsor['acConDate'] = annRepDataSponsor[i]['acConDate']
                    # 实缴出资方式
                    sponsor['acConForm_CN'] = annRepDataSponsor[i]['acConForm_CN']
                    print(sponsor)
                    self.insert_annRepDataSponsor(sponsor, params['main_id'], anCheYear)
            # 股权变更信息
            if 'annRepDataAlterstock' in data.keys():
                annRepDataAlterstock = data['annRepDataAlterstock']
                for i in range(len(annRepDataAlterstock)):
                    alterstock = {}
                    # 变更时间
                    alterstock['altDate'] = annRepDataAlterstock[i]['altDate']
                    # 变更名称
                    alterstock['inv'] = annRepDataAlterstock[i]['inv']
                    # 变更前股权比例
                    alterstock['transAmPr'] = annRepDataAlterstock[i]['transAmPr']
                    # 变更后股权比例
                    alterstock['transAmAft'] = annRepDataAlterstock[i]['transAmAft']
                    print(alterstock)
                    self.insert_annRepDataAlterstock(alterstock, params['main_id'], anCheYear)

    # 插入企业年报基本信息
    def insert_annRepData(self, item, main_id, anCheYear):
        print("mainid: ", main_id)
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_annrepdata(year,c_id, tel,email) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (anCheYear, main_id, item['tel'], item['email']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 插入年报对外投资信息
    def insert_annRepDataInvestment(self, item, main_id, anCheYear):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_annredata_investment(year,c_id, entName,uniscId) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (anCheYear, main_id, item['entName'], item['uniscId']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 插入年报网站或网店信息
    def insert_annRepDataWebsite(self, item, main_id, anCheYear):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_annrepdata_website(year,c_id, webSitName,domain) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (anCheYear, main_id, item['webSitName'], item['domain']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 插入年报股东及出资信息
    def insert_annRepDataSponsor(self, item, main_id, anCheYear):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_annrepdata_sponsor(year,c_id, invName,liSubConAm,subConDate,subConFormName,liAcConAm,acConDate,acConForm_CN) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                anCheYear, main_id, item['invName'], item['liSubConAm'], item['subConDate'], item['subConFormName'],
                item['liAcConAm'], item['acConDate'], item['acConForm_CN']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 插入年报股权变更信息
    def insert_annRepDataAlterstock(self, item, main_id, anCheYear):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_annrepdata_alterstock(year,c_id, altDate,inv,transAmPr,transAmAft) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            db.ping(reconnect=True)
            cursor.execute(sql,
                           (anCheYear, main_id, item['altDate'], item['inv'], item['transAmPr'], item['transAmAft']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 获取股权变更信息
    def get_insAlterstockinfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-insAlterstockinfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('股权变更条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-insAlterstockinfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select inv,altDate,transAmPrBf,transAmPrAf,publicDate from gx_insalterstockinfo'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 股东
                    item['inv'] = data[j]['inv']
                    # 股权变更日期
                    item['altDate'] = data[j]['altDate']
                    # 变更前股权比例
                    item['transAmPrBf'] = data[j]['transAmPrBf']
                    # 变更后股权比例
                    item['transAmPrAf'] = data[j]['transAmPrAf']
                    # 公示日期
                    item['publicDate'] = data[j]['publicDate']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_insAlterstockinfo(item, params['main_id'])

    # 插入股权变更信息
    def insert_insAlterstockinfo(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_insalterstockinfo(c_id, inv,altDate,transAmPrBf,transAmPrAf,publicDate) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            db.ping(reconnect=True)
            cursor.execute(sql, (main_id, item['inv'], item['altDate'], item['transAmPrBf'],
                                 item['transAmPrAf'], item['publicDate']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    # 知识产权出质登记信息
    def get_insProPledgeRegInfo(self, params):
        url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-insProPledgeRegInfo-{}.html?nodeNum={}&entType={}&start=0&sourceType=A'
        url = url.format(
            params['pripid'], params['nodeNum'], params['entType'])
        json_data = self.get_json_data(url)
        print(json_data)
        totalPage = int(json_data['totalPage'])
        recordsTotal = int(json_data['recordsTotal'])
        print('知识产权出质登记信息条数')
        print(recordsTotal)
        index = 0
        for i in range(totalPage):
            if i is not 0:
                index += 5
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-insProPledgeRegInfo-{}.html?nodeNum={}&entType={}&start={}&sourceType=A'.format(
                params['pripid'], params['nodeNum'], params['entType'], str(index))
            print(url)

            u_data = self.get_json_data(url)
            print(u_data)
            data = u_data['data']
            if data is not None:
                bsql = 'select uniscId,entName,kinds,pledgor,pleRegPerFrom,pleRegPerTo,publicDate,tmName,type from gx_inspropledgereginfo'
                b = self.get_bloomFilter(bsql)
                for j in range(len(data)):
                    item = {}
                    # 知识产权登记号
                    item['uniscId'] = data[j]['uniscId']
                    # 名称
                    item['entName'] = data[j]['entName']
                    # 种类
                    item['kinds'] = data[j]['kinds']
                    # 出质人名称
                    item['pledgor'] = data[j]['pledgor']
                    # 质权登记起始日期
                    item['pleRegPerFrom'] = data[j]['pleRegPerFrom']
                    # 质权登记终止日期
                    item['pleRegPerTo'] = data[j]['pleRegPerTo']
                    # 公示日期
                    item['publicDate'] = data[j]['publicDate']
                    # 商标名称
                    item['tmName'] = data[j]['tmName']
                    # 状态
                    item['type'] = data[j]['type']
                    print(item)
                    if item in b:
                        print("已存在数据库")
                    else:
                        b.add(item)
                        self.insert_insProPledgeRegInfo(item, params['main_id'])

    # 插入知识产权出质登记信息
    def insert_insProPledgeRegInfo(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "insert into gx_inspropledgereginfo(c_id, uniscId,entName,kinds,pledgor,pleRegPerFrom,pleRegPerTo,publicDate,tmName,type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            db.ping(reconnect=True)
            cursor.execute(sql, (main_id, item['uniscId'], item['entName'], item['kinds'], item['pledgor'],
                                 item['pleRegPerFrom'], item['pleRegPerTo'], item['publicDate'], item['tmName'],
                                 item['type']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
        return None

    def get_bloomFilter(self, sql):
        bloom = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        desc = cursor.description
        # desc 将会输出  (('total_premium', 246, 7, 26, 26, 2, 0), ('quote_count', 3, 3, 11, 11, 0, 0), ('order_count', 3, 3, 11, 11, 0, 0))
        object_dict = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        # print(object_dict)
        cursor.close()
        for d in object_dict:
            bloom.add(d)
        return bloom

    def get_main_id(self, inv_name):
        global idS
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "select id from gx_holder where inv_name=%s"
        try:
            cursor = db.cursor()
            cursor.execute(sql, inv_name)
            idS = cursor.fetchone()
            if idS:
                print(idS[0])
                idS = int(idS[0])
            db.commit()
            db.close()
        except:
            print("查询数据错误")
        return idS

    def select_main_id(self, entName):
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        sql = "select id from gsxt where entName=%s"
        global idS
        try:
            cursor = db.cursor()
            cursor.execute(sql, entName)
            idS = cursor.fetchone()
            if idS:
                print(idS[0])
                idS = int(idS[0])
            db.commit()
            db.close()
        except:
            print("查询数据错误")
        return idS

    def ExistOrNot(self, jsonObj, key1, key2=None):
        if key1 in jsonObj:
            return jsonObj[key1]
        else:
            if key2 in jsonObj:
                return jsonObj[key2]
            else:
                return None

    @retry(stop_max_attempt_number=100)
    def get_PROXY(self):
        # 获取代理
        json_p = self.ss.getOne('gxst')
        host = str(json_p['ip'])
        port = str(json_p['port'])
        hostport = host + ':' + port
        self.proxy.update({'http': hostport})
        json_ps = self.ss.getOnes('gxst')
        hosts = str(json_ps['ip'])
        ports = str(json_ps['port'])
        hostports = hosts + ':' + ports
        self.proxy.update({'https': hostports})
        print("ip端口响应正常")
        try:
            requests.get('http://app.gsxt.gov.cn/gsxt/pubMsgList.html ', headers=self.headers, proxies=self.proxy,
                         timeout=5, verify=False)
        except:
            self.ss.setFalse(str(json_p['ip']), str(json_p['port']), 'gxst')
            self.ss.setFalse(str(json_ps['ip']), str(json_ps['port']), 'gxst')
            raise Exception
        print(self.proxy)

    def main(self):
        self.get_PROXY()
        print("搜索关键词：", self.searchword)
        search_page = self.get_search_page(self.search_url)
        while (search_page == None):
            search_page = self.get_search_page(self.search_url)
            print(search_page)
            time.sleep(1)
        print(type(search_page))
        data = json.loads(search_page)
        print(data)
        print(type(data))
        # 获取搜索总条数
        recordsTotal = int(data['data']['result']['recordsTotal'])
        print('获取搜索总条数')
        print(recordsTotal)
        perPage = int(data['data']['result']['perPage'])
        pageNum = math.ceil(recordsTotal / perPage)
        print(pageNum)
        if pageNum > 0:
            for i in range(1, pageNum + 1):
                index_url = 'http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page={}'.format(
                    str(i))
                searchpage = self.get_search_page(index_url)
                while (searchpage == None):
                    searchpage = self.get_search_page(index_url)
                    print(searchpage)
                    time.sleep(1)

                data = json.loads(searchpage)
                print(index_url)
                json_data = data['data']['result']['data']
                # print(json_data)
                for j in range(len(json_data)):
                    pripid = json_data[j]['pripid']
                    nodeNum = json_data[j]['nodeNum']
                    entType = json_data[j]['entType']
                    detail_page = self.get_detail_page(pripid, nodeNum, entType)
                    print(type(detail_page))
                    k = 0
                    detail_data = json.loads(detail_page)
                    while ('code' in detail_data and 'data' in detail_data) or ('NGIDERRORCODE' in detail_data):
                        self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'gxst')
                        self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'gxst')
                        self.get_PROXY()

                        detail_page = self.get_detail_page(pripid, nodeNum, entType)
                        detail_data = json.loads(detail_page)
                        k = k + 1
                        print(k)
                        if k > 5:
                            j = j + 1
                            pripid = json_data[j]['pripid']
                            nodeNum = json_data[j]['nodeNum']
                            entType = json_data[j]['entType']
                            detail_page = self.get_detail_page(pripid, nodeNum, entType)
                            detail_data = json.loads(detail_page)
                            k = 0

                    print(detail_page)
                    # detail_data = json.loads(detail_page)
                    print(detail_data)
                    print(type(detail_page))
                    # 企业基本信息
                    items = self.parse_detail_page(detail_page)
                    print(items)
                    params = {}
                    params['pripid'] = detail_data['result']['pripId']
                    params['nodeNum'] = detail_data['result']['nodeNum']
                    params['entType'] = detail_data['result']['entType']
                    entName = items['entName']
                    main_id = self.select_main_id(entName)

                    params['main_id'] = main_id

                    # 股东及出资信息
                    holder_detail = self.get_holder_detail(params)
                    print(holder_detail)
                    # # # 主要人员信息
                    # keyperson = self.get_leader(params)
                    # print(keyperson)
                    # # 分支机构信息
                    entprise_info_branch = self.get_branch(params)
                    # print(entprise_info_branch)
                    # # # 变更信息
                    # entprise_info_after = self.get_entprise_info_after(params)
                    # print(entprise_info_after)
                    # # # 动产抵押登记信息
                    # mortreginfo = self.get_mortreg(params)
                    # print(mortreginfo)
                    # # # 股权出质信息
                    # stakqualitinfo = self.get_stakqualitinfo(params)
                    # print(stakqualitinfo)
                    # # #商标注册信息
                    # trademark = self.get_trademark(params)
                    # print(trademark)
                    # # 司法协助信息
                    # assistInfo = self.get_assistInfo(params)
                    # print(assistInfo)
                    # # 行政许可信息
                    # licenceinfoDetail = self.get_licenceinfoDetail(params)
                    # print(licenceinfoDetail)
                    # # 行政处罚信息
                    # punishmentdetail = self.get_punishmentdetail(params)
                    # print(punishmentdetail)
                    # # 抽查检查结果信息
                    # spotCheckInfo = self.get_spotCheckInfo(params)
                    # print(spotCheckInfo)
                    # # 列入严重违法失信企业名单（黑名单）信息
                    # illInfo = self.get_illInfo(params)
                    # print(illInfo)
                    # # 列入经营异常名录信息
                    # entBusExcep = self.get_entBusExcep(params)
                    # print(entBusExcep)
                    # # 企业年报信息
                    # annualReportInfo = self.get_annualReportInfo(params)
                    # print(annualReportInfo)
                    # # 股权变更信息
                    # insAlterstockinfo = self.get_insAlterstockinfo(params)
                    # print(insAlterstockinfo)
                    # # 知识产权出质登记信息
                    # insProPledgeRegInfo = self.get_insProPledgeRegInfo(params)
                    # print(insProPledgeRegInfo)


if __name__ == '__main__':
    g = GSXT("建设")
    g.main()
