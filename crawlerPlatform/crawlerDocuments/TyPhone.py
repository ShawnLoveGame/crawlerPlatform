# coding=utf-8
import requests
from urllib.parse import quote
from retrying import retry
import json
import math
import time
from html.parser import HTMLParser
from urllib.parse import quote
import re
from requests.exceptions import RequestException
import pymysql
from lxml import etree
import datetime
from crawlerDocuments.SetProxy import Ss
import sys
from functools import singledispatch
import linecache
# from fake_useragent import UserAgent
from pybloom_live import BloomFilter, ScalableBloomFilter


class Tphone():
    def __init__(self, keyword):
        self.ss = Ss()
        self.host = '192.168.1.68'
        # 用户名
        self.user = 'root'
        # 密码
        self.pwd = '123456'
        # 数据库
        self.database = 'phtest'
        self.keyword = keyword
        self.headers = {
            "Accept-Encoding": "gzip",
            "authorization": "0###oo34J0adf6Rzt_aOq30qZvE6TfcY###1553754234924###0ef9bd2f8b46cf3a2d83d9508395cf41",
            # "authorization": "0###oo34J0fWa8KIqCoTbqR0q1nl1jeo###1555306590562###427f95b92edf0bf3de2542b7f15310d7",
            # "authorization": "0###oo34J0fvkeAxvs2cdTSVGphTWDm0###1559206724357###73e1f3bc62a11d4e5e4c94b55ef8eb07",
            "referer": "https://servicewechat.com/wx9f2867fc22873452/21/page-frame.html",
            "content-type": "application/json",
            "version": "TYC-XCX-WX",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/7.0.0(0x17000024) NetType/WIFI Language/zh_CN",
            "Host": "api9.tianyancha.com",
            "Connection": "Keep-Alive",
            # "x-auth-token": "645132"
        }
        self.post_headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wx9f2867fc22873452/22/page-frame.html',
            'authorization': '0###oo34J0adf6Rzt_aOq30qZvE6TfcY###1553754234924###0ef9bd2f8b46cf3a2d83d9508395cf41',
            'version': 'TYC-XCX-WX',
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9s Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 MicroMessenger/7.0.3.1400(0x2700033D) Process/appbrand1 NetType/WIFI Language/zh_CN',
            'Content-Length': '84',
            'Host': 'api9.tianyancha.com',
            'Connection': 'Keep-Alive'
        }
        self.lawsuit_headers = {
            'Host': 'm.tianyancha.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9s Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/673 MMWEBSDK/190102 Mobile Safari/537.36 MMWEBID/671 MicroMessenger/7.0.3.1400(0x2700033D) Process/appbrand1 NetType/WIFI Language/zh_CN miniProgram',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            # 'Cookie': ' aliyungf_tc=AQAAAMyyDRBd8gIAKDWcGy6DgVknkKQS; csrfToken=YoVFiLK_QRUIWzIgiKd8X7hj; TYCID=5be4ab00664511e986bb7f4796e72b60; undefined=5be4ab00664511e986bb7f4796e72b60; ssuid=9428995180',
            'X-Requested-With': 'com.tencent.mm'
        }
        self.abnormal_headers = {
            'Host': 'api9.tianyancha.com',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'version': 'TYC-XCX-WX',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN',
            'Authorization': '0###oo34J0fvkeAxvs2cdTSVGphTWDm0###1559206724357###73e1f3bc62a11d4e5e4c94b55ef8eb07',
            'Referer': 'https://servicewechat.com/wx9f2867fc22873452/26/page-frame.html',
            'Accept-Language': 'zh-cn'
        }
        self.proxy = {}
        self.paramdata = {
            "keyWords": "腾讯科技（深圳）有限公司", "pn": 1, "ps": 20, "casereason": -100}

    @retry(stop_max_attempt_number=100)
    def get_PROXY(self):
        # 获取代理
        json_p = self.ss.getOne('ty')
        host = str(json_p['ip'])
        port = str(json_p['port'])
        hostport = host + ':' + port
        self.proxy.update({'http': hostport})
        json_ps = self.ss.getOnes('ty')
        hosts = str(json_ps['ip'])
        ports = str(json_ps['port'])
        hostports = hosts + ':' + ports
        self.proxy.update({'https': hostports})
        print("ip端口响应正常")
        try:
            requests.get('https://api9.tianyancha.com/', headers=self.headers, proxies=self.proxy, timeout=5,
                         verify=False)
        except:
            self.ss.setFalse(str(json_p['ip']), str(json_p['port']), 'ty')
            self.ss.setFalse(str(json_ps['ip']), str(json_ps['port']), 'ty')
            raise Exception
        # print("该IP可访问网站")
        print(self.proxy)

    def run(self):
        self.get_PROXY()
        # search_list = self.get_search_list()
        index = 1
        # for se in search_list:
        # 判断key的类型
        # if se['scode'] is None:
        #     key = se['com_name']
        #     data_sql="select * from tp_com where com_name='"+key+"'"
        # else:
        #     key = se['scode']
        #     data_sql = "select * from tp_com where creditCode='" + key + "'"
        # if bool(self.ifInDatabase(data_sql)):
        #     print("已存在")
        # else:
        if index % 5 == 0:  # 五条数据换ip
            self.get_PROXY()
        # 计算时间
        start = time.time()
        url = 'https://api9.tianyancha.com/services/v3/search/sNorV3/{}?pageNum=1&pageSize=10&sortType=0'
        # key = sys.argv[1]
        # key = '京东'
        url = url.format(quote(self.keyword))
        print(url)
        html = self.get_index_html(url, self.headers)
        get_url_info = json.loads(html)
        data = get_url_info['data']
        # print(data)
        if data:
            companyTotalPage = int(data['companyTotalPage'])
            if companyTotalPage > 0:
                pagecount = math.ceil(companyTotalPage / 10)
                if pagecount > 10:
                    pagecount = 10
                print("搜索页数")
                print(pagecount)
                for i in range(1, pagecount + 1):
                    url = 'https://api9.tianyancha.com/services/v3/search/sNorV3/{}?pageNum={}&pageSize=10&sortType=0'
                    url = url.format(quote(self.keyword), i)
                    html = self.get_index_html(url, self.headers)
                    get_url_info = json.loads(html)
                    data = get_url_info['data']
                    if data:
                        companyList = data['companyList']
                        company_id_list = []
                        for j in range(len(companyList)):
                            company_id_list.append(companyList[j]['id'])
                        if company_id_list:
                            print(company_id_list)
                            self.get_One_Detail(company_id_list)
        index += 1
        print("搜索条数")
        print(index)
        end = time.time()
        print("搜索速度")
        print(end - start)
        if (end - start) < 60:
            time.sleep(60 - (end - start))
        # print(html)

    def get_One_Detail(self, id_list):
        # 获取数据库数据,放入布隆过滤器
        sql = 'select com_name,legalPersonName,estiblishTime,regNumber,regCapital,actualCapital,creditCode,taxNumber,orgNumber,EName,regStatus,staffNumRange,socialStaffNum,companyOrgType,industry,fromTime,regLocation,approvedTime,regInstitute,businessScope,phoneNumber,email,baseInfo from tp_com'
        b = self.get_bloomFilter(sql)
        for cid in id_list:
            url = 'https://api9.tianyancha.com/services/v3/t/details/appComIcV3/{}?pageSize=1000'
            url = url.format(cid)
            print("单页详细信息url")
            print(url)
            html = self.get_index_html(url, self.headers)
            get_url_info = json.loads(html)
            data = get_url_info['data']
            if data:
                baseInfo = data['baseInfo']
                print("baseInfo : ", baseInfo)
                item = {}
                # 公司名称
                item['com_name'] = self.ExistOrNot(baseInfo, "name")
                # 法定代表人
                item['legalPersonName'] = self.ExistOrNot(baseInfo, "legalPersonName", "legalName")
                # 成立时间
                item['estiblishTime'] = self.ExistOrNot(baseInfo, "estiblishTime")
                # 工商注册号
                item['regNumber'] = self.ExistOrNot(baseInfo, "regNumber")
                # 注册资本
                item['regCapital'] = self.ExistOrNot(baseInfo, "regCapital")
                # 实缴资本
                item['actualCapital'] = self.ExistOrNot(baseInfo, "actualCapital")
                # 统一社会信用代码
                item['creditCode'] = self.ExistOrNot(baseInfo, "creditCode")
                # 纳税人识别号
                item['taxNumber'] = self.ExistOrNot(baseInfo, "taxNumber")
                # 组织机构代码
                item['orgNumber'] = self.ExistOrNot(baseInfo, "orgNumber")
                # 英文名
                item['EName'] = self.ExistOrNot(baseInfo, "property3", "nameEn")
                # 经营状态
                item['regStatus'] = self.ExistOrNot(baseInfo, "regStatus")
                # 人员规模
                item['staffNumRange'] = self.ExistOrNot(baseInfo, "staffNumRange")
                # 参保人数
                item['socialStaffNum'] = self.ExistOrNot(baseInfo, "socialStaffNum")
                # 企业类型
                item['companyOrgType'] = self.ExistOrNot(baseInfo, "companyOrgType")
                # 行业
                item['industry'] = self.ExistOrNot(baseInfo, "industry")
                # 营业期限
                item['fromTime'] = self.ExistOrNot(baseInfo, "fromTime")
                # 注册地址
                item['regLocation'] = self.ExistOrNot(baseInfo, "regLocation", "address")
                # 核准日期
                item['approvedTime'] = self.ExistOrNot(baseInfo, "approvedTime")
                # 登记机关
                item['regInstitute'] = self.ExistOrNot(baseInfo, "regInstitute")
                # 经营范围
                item['businessScope'] = self.ExistOrNot(baseInfo, "businessScope", "scope")
                # 电话
                item['phoneNumber'] = self.ExistOrNot(baseInfo, "phoneNumber")
                # email
                item['email'] = self.ExistOrNot(baseInfo, "email")
                # 简介
                item['baseInfo'] = self.ExistOrNot(baseInfo, "baseInfo")
                item['ty_update_time'] = self.ExistOrNot(baseInfo, "updatetime")
                timeStamp = float(int(item['ty_update_time']) / 1000)
                timeArray = time.localtime(timeStamp)
                item['ty_update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # print(item)
                # 判断是否存在数据库
                print("布隆过滤器")
                # print(item)
                #                 # time.sleep(10)
                if item in b:
                    # print(item)
                    print("已在数据库")
                else:
                    # 插入数据库
                    print("插入数据库")
                    self.insert_date(item)

                sql = "select id from tp_com where com_name='" + item['com_name'] + "' ORDER BY id DESC LIMIT 1"
                print(sql)
                main_id = self.select_main_id(sql)
                # 股东信息
                self.get_holder(data['investorList'], main_id)
                # 分支机构
                self.get_branch(data['branchList'], main_id)
                # # 主要人员
                # self.get_staff(data['staffList'], main_id)
                # # 变更信息
                # self.get_change(data['comChanInfoList'], main_id)
                # # 投资信息
                # self.get_invest(cid, main_id)
                # # 开庭公告
                # self.get_announcement(cid, main_id)
                # # 法律诉讼
                # self.get_lawsuit(item['com_name'], main_id)
                # # 法院公告
                # self.get_court(item['com_name'], main_id)
                # # 失信信息
                # self.get_dishonest(item['com_name'], main_id)
                # # 被执行人信息
                # self.get_zhixing(cid, main_id)
                # # 司法协助信息
                # self.get_judicial(cid, main_id)
                # # 行政处罚信息
                # self.get_punishment(cid, item['com_name'], main_id)
                # # 严重违法
                # self.get_illegal(item['com_name'], main_id)
                # # 经营异常
                # self.abnormal(cid, item['com_name'])
                # # # 股权出质
                # self.get_companyEquity(item['com_name'], main_id)
                # # 动产抵押
                # self.get_companyMortgage(item['com_name'], main_id)
                # # 知识产权出质
                # self.get_getPledgeReg(cid, main_id)
                # # 司法拍卖
                # self.get_judicialSale(cid, main_id)
                # # 微信公众号信息
                # self.get_wechat(cid, main_id)
                # # 招聘信息
                # self.get_zhaopin(item['com_name'])
                # # 行政许可
                # self.get_license(cid, item['com_name'])
                # # 税务评级
                # self.get_taxcred(cid, item['com_name'])
                # # 抽查检查
                # self.get_checkInfo(item['com_name'])
                # # 资质证书
                # self.get_certificate(cid, item['com_name'])
                # # 招投标
                # self.get_bid(cid, item['com_name'])
                # # 产品信息
                # self.get_appbkinfo(cid, item['com_name'])
                # # 商标信息
                # self.get_tmInfo(cid, item['com_name'])
                # # 专利信息
                # self.get_patent(cid, item['com_name'])
                # # 软件著作权
                # self.get_copyReg(cid, item['com_name'])
                # # 作品著作权
                # self.get_copyrightWork(cid, item['com_name'])
                # # 网站备案信息
                # self.get_icp(cid, item['com_name'])
                # # 历史股东信息
                # self.get_holder_auth(cid, item['com_name'])
                # # 历史对外投资
                # self.get_invest_auth(cid, main_id)
                # # 历史开庭公告
                # self.get_court_auto(cid, item['com_name'])
                # # 历史出质信息
                # self.get_Equity_auto(cid, item['com_name'])
                # # 历史行政许可信息(信用中国)
                # self.get_license_auto(cid, item['com_name'])
                # #  历史行政许可信息(工商局)
                # self.get_PastLicense_auto(cid, item['com_name'])

    def abnormal(self, cid, com_name):
        print("cid ", cid)
        print("获取经营异常信息")
        url = 'https://api9.tianyancha.com/services/v3/expanse/abnormal?id={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.abnormal_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totalcount = data['total']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 20)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(cid, page), headers=self.headers)
                        if json.loads(resp)['state'] == 'ok':
                            pun_data = json.loads(resp)['data']
                            if pun_data:
                                result_list = pun_data['result']
                                for result in result_list:
                                    item = {}
                                    # 列入日期
                                    item['putDate'] = result['putDate']
                                    # 列入原因
                                    item['putReason'] = result['putReason']
                                    # 列入机关
                                    item['putDepartment'] = result['putDepartment']
                                    item['removeDate'] = None
                                    item['removeReason'] = None
                                    item['removeDepartment'] = None
                                    if 'removeDate' in result:
                                        item['removeDate'] = result['removeDate']
                                    if 'removeReason' in result:
                                        item['removeReason'] = result['removeReason']
                                    if 'removeDepartment' in result:
                                        item['removeDepartment'] = result['removeDepartment']
                                    print(item)
                                    self.insert_abnormal(item, com_name)

    def insert_abnormal(self, item, com_name):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_abnormal(com_name, putDate, putReason, putDepartment, removeDate, removeReason, removeDepartment) values (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                com_name, item['putDate'], item['putReason'], item['putDepartment'], item['removeDate'],
                item['removeReason'], item['removeDepartment']))
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_tmInfo(self, id, com_name):
        print('获取商标信息')
        url = 'https://api9.tianyancha.com/services/v3/trademark/tms.json'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.post_tmInfo_html(url, id, 1)
        json_data = json.loads(html)
        print("get_tmInfo data : ", json_data)
        if json_data['state'] == 'ok':
            data = json_data['data']
            print(data)
            if data['items']:
                totalcount = data['total']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 20)
                    for page in range(1, pagecount + 1):
                        resp = self.post_tmInfo_html(url, id, page)
                        if json.loads(resp)['state'] == 'ok':
                            pun_data = json.loads(resp)['data']
                            if pun_data:
                                items = pun_data['items']
                                if items:
                                    for item in items:
                                        # 商标名称
                                        try:
                                            tmName = item['tmName']
                                        except:
                                            tmName = ''
                                        # 商标类型
                                        try:
                                            intCls = item['intCls']
                                        except:
                                            intCls = ''
                                        # 注册号
                                        try:
                                            regNo = item['regNo']
                                        except:
                                            regNo = ''
                                        # 申请时间
                                        try:
                                            appDate = item['appDate']
                                        except:
                                            appDate = ''
                                        # 状态
                                        try:
                                            status = item['status']
                                        except:
                                            status = ''
                                        # 申请人
                                        try:
                                            applicantCn = item['applicantCn']
                                        except:
                                            applicantCn = ''
                                        # 申请流程
                                        try:
                                            category = item['category']
                                        except:
                                            category = ''
                                        # 商标url
                                        try:
                                            tmPic = item['tmPic']
                                        except:
                                            tmPic = ''
                                        args = (
                                            com_name, tmName, intCls, regNo, appDate, status, applicantCn, category,
                                            tmPic)
                                        self.insert_tmInfo(args)

    def insert_tmInfo(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_tmInfo(com_name, tmName, intCls, regNo, appDate, status, applicantCn, category, tmPic) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_license_auto(self, id, com_name):
        print('获取历史行政许可信息(信用中国)')
        url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getPastLicenseCN?cId={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totalcount = data['totalCount']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if json.loads(resp)['state'] == 'ok':
                            pun_data = json.loads(resp)['data']
                            if pun_data:
                                items = pun_data['list']
                                if items:
                                    for item in items:
                                        # 许可文书号
                                        try:
                                            licenceNumber = item['licenceNumber']
                                        except:
                                            licenceNumber = '-'
                                        # 法人代表姓名
                                        try:
                                            legalPersonName = item['legalPersonName']
                                        except:
                                            legalPersonName = '-'
                                        # 审核类型
                                        try:
                                            audiType = item['audiType']
                                        except:
                                            audiType = '-'
                                        # 许可有效期
                                        try:
                                            validityTime = item['validityTime']
                                        except:
                                            validityTime = '-'
                                        # 许可决定日期
                                        try:
                                            decisionDate = item['decisionDate']
                                        except:
                                            decisionDate = '-'
                                        # 许可截止日期
                                        try:
                                            endDate = item['endDate']
                                        except:
                                            endDate = '-'
                                        # 地方编码
                                        try:
                                            localCode = item['localCode']
                                        except:
                                            localCode = '-'
                                        # 许可机关
                                        try:
                                            department = item['department']
                                        except:
                                            department = '-'
                                        # 许可内容
                                        try:
                                            licenceContent = item['licenceContent']
                                        except:
                                            licenceContent = '-'
                                        args = (
                                            com_name, licenceNumber, legalPersonName, audiType, validityTime,
                                            decisionDate,
                                            endDate, localCode, department, licenceContent)
                                        self.insert_getLicenseCreditchina(args)

    def get_PastLicense_auto(self, id, com_name):
        print('获取历史行政许可信息(工商局)')
        url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getPastLicense?cId={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totaleCount = data['totalCount']
                if totaleCount:
                    pageCount = math.ceil(totaleCount / 20)
                    if pageCount:
                        for page in range(1, pageCount + 1):
                            resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                            if resp:
                                gs_json_data = json.loads(resp)['data']
                                gs_dataList = gs_json_data['list']
                                if gs_dataList:
                                    for gs_data in gs_dataList:
                                        # 许可文件编号
                                        licencenumber = gs_data['licencenumber']
                                        # 许可文件名称
                                        licencename = gs_data['licencename']
                                        # 有效期自
                                        fromdate = gs_data['fromdate']
                                        # 有效期至
                                        todate = gs_data['todate']
                                        # 许可机关
                                        department = gs_data['department']
                                        # 许可内容
                                        scope = gs_data['scope']
                                        args = (
                                            com_name, licencenumber, licencename, fromdate, todate, department, scope)
                                        self.insert_getLicense(args)

    def get_Equity_auto(self, id, com_name):
        print('获取历史出质信息')
        url = 'https://api9.tianyancha.com/services/v3/past/companyEquity?id={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totalcount = data['count']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if json.loads(resp)['state'] == 'ok':
                            eq_data = json.loads(resp)['data']
                            if eq_data:
                                items = eq_data['items']
                                if items:
                                    for item in items:
                                        # 登记编号
                                        try:
                                            regNumber = item['regNumber']
                                        except:
                                            regNumber = '-'
                                        # 状态
                                        try:
                                            state = item['state']
                                        except:
                                            state = '-'
                                        # 出质人
                                        try:
                                            pledgorStr = item['pledgorStr']
                                        except:
                                            pledgorStr = '-'
                                        # 出质人证件号码
                                        try:
                                            certifNumber = item['certifNumber']
                                        except:
                                            certifNumber = '-'
                                        # 出质股权数
                                        try:
                                            equityAmount = item['equityAmount']
                                        except:
                                            equityAmount = '-'
                                        # 质权人
                                        try:
                                            pledgee = item['pledgee']
                                        except:
                                            pledgee = '-'
                                        # 质权人证件号码
                                        try:
                                            certifNumberR = item['certifNumberR']
                                        except:
                                            certifNumberR = '-'
                                        # 股权出质登记日期
                                        try:
                                            regDate = item['regDate']
                                        except:
                                            regDate = '-'
                                        args = (
                                            com_name, regNumber, state, pledgorStr, certifNumber, equityAmount, pledgee,
                                            certifNumberR, regDate)
                                        self.insert_Equity_auto(args)
        # db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        # sql = """insert into tp_Equity_auto(com_name, regNumber, state, pledgorStr, certifNumber, equityAmount, pledgee, certifNumberR, regDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # try:
        #     cursor = db.cursor()
        #     cursor.execute(sql, args)
        #     db.commit()
        #     cursor.close()
        #     db.close()
        # except RequestException as err:
        #     print(err)

    def insert_Equity_auto(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_Equity_auto(com_name, regNumber, state, pledgorStr, certifNumber, equityAmount, pledgee, certifNumberR, regDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_court_auto(self, id, com_name):
        print('获取历史法院公告')
        url = 'https://api9.tianyancha.com/services/v3/past/courtV2?id={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            totalcount = json_data['total']
            if totalcount:
                pagecount = math.ceil(int(totalcount) / 20)
                for page in range(1, pagecount + 1):
                    resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                    if json.loads(resp)['state'] == 'ok':
                        items = json.loads(resp)['courtAnnouncements']
                        if items:
                            for item in items:
                                # 当事人
                                try:
                                    party2 = item['party2']
                                except:
                                    party2 = '-'
                                # 上诉方
                                try:
                                    party1 = item['party1']
                                except:
                                    party1 = '-'
                                # 公告类型
                                try:
                                    bltntypename = item['bltntypename']
                                except:
                                    bltntypename = '-'
                                # 刊登日期
                                try:
                                    publishdate = item['publishdate']
                                except:
                                    publishdate = '-'
                                # 刊登版面
                                try:
                                    publishpage = item['publishpage']
                                except:
                                    publishpage = '-'
                                # 法院
                                try:
                                    courtcode = item['courtcode']
                                except:
                                    courtcode = '-'
                                # 公告内容
                                try:
                                    content = item['content']
                                except:
                                    content = '-'

                                args = (
                                    com_name, party2, party1, bltntypename, publishdate, publishpage, courtcode,
                                    content)
                                self.insert_court_auto(args)

    def insert_court_auto(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_court_auto(com_name, party2, party1, bltntypename, publishdate, publishpage, courtcode, content) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_invest_auth(self, id, main_id):
        print('获取历史对外投资信息')
        url = 'https://api9.tianyancha.com/services/v3/past/invest?id={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totalcount = data['total']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 20)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if json.loads(resp)['state'] == 'ok':
                            copy_data = json.loads(resp)['data']
                            if copy_data:
                                items = copy_data['result']
                                if items:
                                    for item in items:
                                        # 投资公司
                                        try:
                                            com_name = item['name']
                                        except:
                                            com_name = '-'
                                        # 投资金额
                                        try:
                                            invest_amount = item['amount']
                                        except:
                                            invest_amount = '-'
                                        # 投资比例
                                        try:
                                            invert_percent = item['percent']
                                        except:
                                            invert_percent = '-'
                                        # 公司类型
                                        try:
                                            orgType = item['orgType']
                                        except:
                                            orgType = '-'
                                        # 经营范围
                                        try:
                                            business_scope = item['business_scope']
                                        except:
                                            business_scope = '-'
                                        # 公司状态
                                        try:
                                            regStatus = item['regStatus']
                                        except:
                                            regStatus = '-'
                                        # 别名
                                        try:
                                            alias = item['alias']
                                        except:
                                            alias = '-'
                                        # 创建时间
                                        try:
                                            estiblishTime = item['estiblishTime']
                                        except:
                                            estiblishTime = '-'
                                        # 法人代表
                                        try:
                                            legalPersonName = item['legalPersonName']
                                        except:
                                            legalPersonName = '-'
                                        # 行业
                                        try:
                                            category = item['category']
                                        except:
                                            category = '-'
                                        # 注册资本
                                        try:
                                            regCapital = item['regCapital']
                                        except:
                                            regCapital = '-'
                                        # 社会统一信用代码
                                        try:
                                            creditCode = item['creditCode']
                                        except:
                                            creditCode = '-'
                                        args = (
                                            main_id, com_name, invest_amount, invert_percent, orgType, business_scope,
                                            regStatus, alias, estiblishTime, legalPersonName, category, regCapital,
                                            creditCode)
                                        self.insert_invest_auto(args)

    def insert_invest_auto(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_invest(c_id, com_name, invest_amount, invest_percent, orgType, business_scope, regStatus, alias, estiblishTime, legalPersonName, category, regCapital, creditCode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_holder_auth(self, id, com_name):
        print('获取历史股东信息')
        url = 'https://api9.tianyancha.com/services/v3/past/holder?id={}&pageNum={}&pageSize=20&auth=0'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                totalcount = data['total']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 20)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if json.loads(resp)['state'] == 'ok':
                            copy_data = json.loads(resp)['data']
                            if copy_data:
                                items = copy_data['result']
                                if items:
                                    for item in items:
                                        # 历史股东
                                        try:
                                            auth_name = item['name']
                                        except:
                                            auth_name = '-'
                                        # 公司数
                                        try:
                                            toco = item['toco']
                                        except:
                                            toco = '-'
                                        capitals = item['capital'][0]
                                        try:
                                            amomon = capitals['amomon']
                                        except:
                                            amomon = '-'
                                        try:
                                            h_time = capitals['time']
                                        except:
                                            h_time = '-'
                                        # 持股比例
                                        try:
                                            percent = capitals['percent']
                                        except:
                                            percent = '-'
                                        try:
                                            paymet = capitals['paymet']
                                        except:
                                            paymet = '-'
                                        args = (com_name, auth_name, toco, amomon, h_time, percent, paymet)
                                        self.insert_holder_auth(args)

    def insert_holder_auth(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_holder_auth(com_name, auth_name, toco, amomon, h_time, percent, paymet) values (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_icp(self, id, com_name):
        print('获取网站备案信息')
        url = 'https://api9.tianyancha.com/services/v3/ar/icp/{}.json'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            if json_data['state'] == 'ok':
                datas = json_data['data']
                if datas:
                    for data in datas:
                        # 网址名称
                        try:
                            webName = data['webName']
                        except:
                            webName = '-'
                        # 网站首页
                        try:
                            webSite = data['webSite'][0]
                        except:
                            webSite = '-'
                        # 审核时间
                        try:
                            examineDate = data['examineDate']
                        except:
                            examineDate = '-'
                        # 备案号
                        try:
                            liscense = data['liscense']
                        except:
                            liscense = '-'
                        # 主办单位性质
                        try:
                            companyType = data['companyType']
                        except:
                            companyType = '-'
                        args = (com_name, webName, webSite, examineDate, liscense, companyType)
                        self.insert_icp(args)

    def insert_icp(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_icp(com_name, webName, webSite, examineDate, liscense, companyType) values (%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_copyrightWork(self, id, com_name):
        print('获取作品著作权')
        url = 'https://api9.tianyancha.com/services/v3/expanse/copyrightWorks?id={}&pageSize=10&pageNum={}'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalcount = data['count']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if resp:
                            copy_data = json.loads(resp)['data']
                            if copy_data:
                                items = copy_data['resultList']
                                if items:
                                    for item in items:
                                        # 作品名称
                                        try:
                                            fullname = item['fullname']
                                        except:
                                            fullname = '-'
                                        # 登记号
                                        try:
                                            regnum = item['regnum']
                                        except:
                                            regnum = '-'
                                        # 作品类别
                                        try:
                                            full_type = item['type']
                                        except:
                                            full_type = '-'
                                        # 创作完成日期
                                        try:
                                            finishTime = item['finishTime']
                                        except:
                                            finishTime = '-'
                                        # 首次发表日期
                                        try:
                                            publishtime = item['publishtime']
                                        except:
                                            publishtime = '-'
                                        # 登记日期
                                        try:
                                            regtime = item['regtime']
                                        except:
                                            regtime = '-'
                                        # 著作权人信息
                                        try:
                                            author = item['authorNationality']
                                        except:
                                            author = '-'
                                        args = (
                                            com_name, fullname, regnum, full_type, finishTime, publishtime, regtime,
                                            author)
                                        self.insert_copyrightWork(args)

    def insert_copyrightWork(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_copyrightWork(com_name, fullname, regnum, full_type, finishTime, publishtime, regtime, author) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_copyReg(self, id, com_name):
        print('获取软件著作权信息')
        url = 'https://api9.tianyancha.com/services/v3/expanse/copyReg?id={}&pageSize=10&pageNum={}'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalcount = data['viewtotal']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if resp:
                            copy_data = json.loads(resp)['data']
                            if copy_data:
                                items = copy_data['items']
                                if items:
                                    for item in items:
                                        # 软件名称
                                        try:
                                            fullname = item['fullname']
                                        except:
                                            fullname = '-'
                                        # 登记号
                                        try:
                                            regnum = item['regnum']
                                        except:
                                            regnum = '-'
                                        # 作品类别
                                        try:
                                            full_type = item['type']
                                        except:
                                            full_type = '-'
                                        # 创作完成日期
                                        try:
                                            finishDate = item['finishDate']
                                        except:
                                            finishDate = '-'
                                        # 首次发表日期
                                        try:
                                            publishtime = item['publishtime']
                                            if publishtime:
                                                timeArray = time.localtime(int(publishtime) / 1000)
                                                publishtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                        except:
                                            publishtime = '-'
                                        # 登记批准日期
                                        try:
                                            regtime = item['regtime']
                                            if regtime != None:
                                                timeArray = time.localtime(int(regtime) / 1000)
                                                regtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                        except:
                                            regtime = '-'

                                        # 软件简称
                                        try:
                                            simplename = item['simplename']
                                        except:
                                            simplename = '-'
                                        # 分类号
                                        try:
                                            catnum = item['catnum']
                                        except:
                                            catnum = '-'
                                        # 版本号
                                        try:
                                            version = item['version']
                                        except:
                                            version = '-'
                                        # 著作权人
                                        try:
                                            author = item['authorNationality']
                                        except:
                                            author = '-'
                                        args = (com_name, fullname, regnum, full_type, finishDate, publishtime, regtime,
                                                simplename, catnum, version, author)
                                        self.insert_copyReg(args)

    def insert_copyReg(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_copyReg(com_name, fullname, regnum, full_type, finishDate, publishtime, regtime, simplename, catnum, version, author) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_patent(self, id, com_name):
        print('获取专利信息')
        url = 'https://api9.tianyancha.com/services/v3/expanse/patent?id={}&pageSize=10&pageNum={}'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalcount = data['viewtotal']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if resp:
                            app_data = json.loads(resp)['data']
                            if app_data:
                                items = app_data['items']
                                if items:
                                    for item in items:
                                        print(item)
                                        # 专利名称
                                        patentName = self.ExistOrNot(item, 'patentName')
                                        # 申请号
                                        appnumber = self.ExistOrNot(item, 'appnumber')
                                        # 公开号
                                        pubnumber = self.ExistOrNot(item, 'pubnumber')
                                        # 分类号
                                        mainCatNum = None
                                        if item['mainCatNum']:
                                            mainCatNum = item['mainCatNum'][0]
                                        # 申请日
                                        applicationTime = self.ExistOrNot(item, 'applicationTime')
                                        # 公开（公告）日
                                        applicationPublishTime = self.ExistOrNot(item, 'applicationPublishTime')
                                        # 申请(专利权)人
                                        applicantname = self.ExistOrNot(item, 'applicantname')
                                        # 发明人
                                        inventor = self.ExistOrNot(item, 'inventor')
                                        # 代理人
                                        agent = self.ExistOrNot(item, 'agent')
                                        # 代理机构
                                        agency = self.ExistOrNot(item, 'agency')
                                        # 地址
                                        address = self.ExistOrNot(item, 'address')
                                        # 摘要
                                        abstracts = self.ExistOrNot(item, 'abstracts')
                                        # 附图
                                        imgUrl = self.ExistOrNot(item, 'imgUrl')
                                        args = (com_name, patentName, appnumber, pubnumber, mainCatNum, applicationTime,
                                                applicationPublishTime, applicantname, inventor, agent, agency, address,
                                                abstracts, imgUrl)
                                        self.insert_patent(args)

    def insert_patent(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_patent(com_name, patentName, appnumber, pubnumber, mainCatNum, applicationTime, applicationPublishTime, applicantname, inventor, agent, agency, address, abstracts, imgUrl) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_appbkinfo(self, id, com_name):
        print('获取产品信息')
        url = 'https://api9.tianyancha.com/services/v3/ar/appbkinfo?id={}&pageSize=10&pageNum={}'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalcount = data['count']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    if pagecount:
                        for page in range(1, pagecount + 1):
                            resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                            if resp:
                                app_data = json.loads(resp)['data']
                                if app_data:
                                    items = app_data['items']
                                    if items:
                                        for item in items:
                                            # 产品名称
                                            app_name = item['name']
                                            # 简称
                                            filterName = item['filterName']
                                            # 类型
                                            classes = item['classes']
                                            # 描述
                                            brief = item['brief']
                                            # 图标
                                            icon = item['icon']
                                            # 分类
                                            pro_type = item['type']
                                            args = (com_name, app_name, filterName, classes, brief, icon, pro_type)
                                            self.insert_product(args)

    def insert_product(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_product(com_name, app_name, filterName, classes, brief, icon, pro_type) values (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_bid(self, id, com_name):
        url = 'https://api9.tianyancha.com/services/v3/expanse/bid?id={}&pageSize=10&pageNum={}'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalcount = data['viewtotal']
                if totalcount:
                    pagecount = math.ceil(int(totalcount) / 10)
                    if pagecount:
                        for page in range(1, pagecount + 1):
                            resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                            if resp:
                                bid_data = json.loads(resp)['data']
                                if bid_data:
                                    items = bid_data['items']
                                    if items:
                                        for item in items:
                                            # 标题
                                            title = item['title']
                                            # 发布时间
                                            publishTime = item['publishTime']
                                            if publishTime:
                                                timeArray = time.localtime(int(publishTime) / 1000)
                                                publishTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                            # 购买者
                                            purchaser = item['purchaser']
                                            # 代理人
                                            proxy = item['proxy']
                                            # 招标公告内容
                                            pat = re.compile('>(.*?)<')
                                            # sss = ''.join(pat.findall(test))
                                            content = ''.join(pat.findall(item['content']))
                                            # 公告详情url
                                            bidUrl = item['bidUrl']
                                            args = (com_name, title, publishTime, purchaser, proxy, content, bidUrl)
                                            self.insert_bid(args)

    def insert_bid(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_bid(com_name, title, publishTime, purchaser, proxy, content, bidUrl) values (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_certificate(self, id, com_name):
        print('获取资质证书信息')
        url = 'https://api9.tianyancha.com/services/v3/expanse/certificate?id={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalCount = data['count']
                if totalCount:
                    pagecount = math.ceil(totalCount / 20)
                    for page in range(1, pagecount + 1):
                        resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                        if resp:
                            ce_data = json.loads(resp)['data']
                            if ce_data:
                                resultList = ce_data['resultList']
                                if resultList:
                                    for result in resultList:
                                        # 详情页id
                                        try:
                                            detail_id = result['id']
                                        except:
                                            detail_id = '-'
                                        # 证书名称
                                        try:
                                            certificateName = result['certificateName']
                                        except:
                                            certificateName = '-'
                                        # 许可证编号
                                        try:
                                            certNo = result['certNo']
                                        except:
                                            certNo = '-'
                                        # 发证日期
                                        try:
                                            startDate = result['startDate']
                                        except:
                                            startDate = '-'
                                        # 有效期至
                                        try:
                                            endDate = result['endDate']
                                        except:
                                            endDate = '-'

                                        args = (com_name, certificateName, certNo, startDate, endDate, detail_id)
                                        self.insert_certificate(args)

    def insert_certificate(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_certificate(com_name, certificateName, certNo, startDate, endDate, detail_id) values (%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_checkInfo(self, com_name):
        print('获取抽查检查信息')
        url = 'https://api9.tianyancha.com/services/v3/ar/checkInfoList?name={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(com_name, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totaleCount = data['count']
                if totaleCount:
                    pageCount = math.ceil(totaleCount / 20)
                    if pageCount:
                        for page in range(1, pageCount + 1):
                            resp = self.get_index_html(url=url.format(com_name, page), headers=self.headers)
                            if resp:
                                ch_data = json.loads(resp)['data']
                                if ch_data:
                                    items = ch_data['items']
                                    if items:
                                        for item in items:
                                            print(item)
                                            # 检查实施机关
                                            checkOrg = item['checkOrg']
                                            # 结果
                                            checkResult = item['checkResult']
                                            # 检查时间
                                            checkDate = item['checkDate']
                                            # 检查类型
                                            checkType = item['checkType']
                                            args = (com_name, checkOrg, checkResult, checkDate, checkType)
                                            self.insert_check(args)

    def insert_check(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_check(com_name, checkOrg, checkResult, checkDate, checkType) values (%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_taxcred(self, id, com_name):
        # 获取税务评级信息
        print('获取税务评级信息')
        url = 'https://api9.tianyancha.com/services/v3/ar/taxcred?id={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totaleCount = data['count']
                if totaleCount:
                    pageCount = math.ceil(totaleCount / 20)
                    if pageCount:
                        for page in range(1, pageCount + 1):
                            resp = self.get_index_html(url=url.format(id, page), headers=self.headers)
                            if resp:
                                ta_data = json.loads(resp)['data']
                                if ta_data:
                                    items = ta_data['items']
                                    if items:
                                        for item in items:
                                            # 纳税人识别号
                                            idNumber = item['idNumber']
                                            # 识别年份
                                            years = item['year']
                                            # 评价部门
                                            evalDepartment = item['evalDepartment']
                                            # 识别等级
                                            grade = item['grade']
                                            # 识别类型
                                            iden_type = item['type']
                                            args = (com_name, idNumber, years, evalDepartment, grade, iden_type)
                                            self.insert_taxcred(args)

    def insert_taxcred(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_taxcred(com_name, idNumber, years, evalDepartment, grade, iden_type) values (%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_license(self, id, com_name):
        # 获取工商行政许可信息
        print(f'获取行政信息(工商局)')
        url_gs = 'https://api9.tianyancha.com/services/v3/aboutCompany/getLicense?cId={}&pageNum={}&pageSize=20'
        url_xy = 'https://api9.tianyancha.com/services/v3/aboutCompany/getLicenseCreditchina?cId={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url_gs.format(id, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totaleCount = data['totalCount']
                if totaleCount:
                    pageCount = math.ceil(totaleCount / 20)
                    if pageCount:
                        for page in range(1, pageCount + 1):
                            resp = self.get_index_html(url=url_gs.format(id, page), headers=self.headers)
                            if resp:
                                gs_json_data = json.loads(resp)['data']
                                gs_dataList = gs_json_data['list']
                                if gs_dataList:
                                    for gs_data in gs_dataList:
                                        # 许可文件编号
                                        licencenumber = gs_data['licencenumber']
                                        # 许可文件名称
                                        licencename = gs_data['licencename']
                                        # 有效期自
                                        fromdate = gs_data['fromdate']
                                        # 有效期至
                                        todate = gs_data['todate']
                                        # 许可机关
                                        department = gs_data['department']
                                        # 许可内容
                                        scope = gs_data['scope']
                                        args = (
                                            com_name, licencenumber, licencename, fromdate, todate, department, scope)
                                        self.insert_getLicense(args)
        xy_html = self.get_index_html(url_xy.format(id, 1), self.post_headers)
        json_data_xy = json.loads(xy_html)
        if json_data_xy:
            data_xy = json_data_xy['data']
            if data_xy:
                totaleCount = data_xy['totalCount']
                if totaleCount:
                    pageCount = math.ceil(totaleCount / 20)
                    if pageCount:
                        for page in range(1, pageCount + 1):
                            resp = self.get_index_html(url=url_xy.format(id, page), headers=self.headers)
                            if resp:
                                xy_json_data = json.loads(resp)['data']
                                xy_dataList = xy_json_data['list']
                                if xy_dataList:
                                    for xy_data in xy_dataList:
                                        print(xy_data)
                                        # 许可文书号
                                        licenceNumber = xy_data['licenceNumber']
                                        # 法人代表名字
                                        legalPersonName = None
                                        if 'legalPersonName' in xy_data:
                                            legalPersonName = xy_data['legalPersonName']
                                        # 审核类型
                                        audiType = xy_data['audiType']
                                        # 许可有效期
                                        validityTime = xy_data['validityTime']
                                        # 许可决定日期
                                        decisionDate = xy_data['decisionDate']
                                        # 许可截止日期
                                        try:
                                            endDate = xy_data['endDate']
                                        except Exception:
                                            endDate = ''
                                        # 地方编码
                                        localCode = xy_data['localCode']
                                        # 许可机关
                                        department = xy_data['department']
                                        # 许可内容
                                        licenceContent = xy_data['licenceContent']
                                        args1 = (
                                            com_name, licenceNumber, legalPersonName, audiType, validityTime,
                                            decisionDate,
                                            endDate, localCode, department, licenceContent)
                                        self.insert_getLicenseCreditchina(args1)

    def insert_getLicenseCreditchina(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_getLicenseCreditchina(com_name, licenceNumber, legalPersonName, audiType, validityTime, decisionDate, endDate, localCode, department, licenceContent) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def insert_getLicense(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_getLicense(com_name, licencenumber, licencename, fromdate, todate, department, scope) values (%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def get_wechat(self, cid, main_id):
        # 获取公众号信息
        print('获取公众号信息')
        url = 'https://api9.tianyancha.com/services/v3/expanse/publicWeChat?id={}&pageNum={}&pageSize=10'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalCount = data['count']
                if totalCount:
                    pageCount = math.ceil(totalCount / 10)
                    for page in range(1, pageCount + 1):
                        resp = self.get_index_html(url.format(cid, page), headers=self.post_headers)
                        if resp:
                            j_data = json.loads(resp)
                            data = j_data['data']
                            resultList = data['resultList']
                            if resultList:
                                for result in resultList:
                                    item = {}
                                    # 昵称
                                    item['title'] = result['title']
                                    # 公众号
                                    item['publicNum'] = result['publicNum']
                                    # 二维码链接
                                    item['codeImg'] = result['codeImg']
                                    # 公众号头像
                                    item['titleImgURL'] = result['titleImgURL']
                                    # 公众号简介
                                    item['recommend'] = result['recommend']
                                    self.insert_wechat(item, main_id)
                        print(f'第{page}页插入完毕！！！')

    def get_zhaopin(self, com_name):
        # 获取招聘信息
        print('获取招聘信息')
        url = 'https://api9.tianyancha.com/services/v3/expanse/getCompanyEmploymentList?companyName={}&pageNum={}&pageSize=6'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(com_name, 1), self.post_headers)
        json_data = json.loads(html)
        if json_data:
            data = json_data['data']
            if data:
                totalCount = data['totalRows']
                if totalCount:
                    pageCount = math.ceil(totalCount / 6)
                    for page in range(1, pageCount + 1):
                        resp = self.get_index_html(url=url.format(com_name, page), headers=self.headers)
                        if resp:
                            z_json_data = json.loads(resp)
                            companyEmploymentList = z_json_data['data']['companyEmploymentList']
                            if companyEmploymentList:
                                for com_post in companyEmploymentList:
                                    print("zhaoping: ", com_post)
                                    # 岗位名称
                                    title = com_post['title']
                                    # 工资
                                    oriSalary = com_post['oriSalary']
                                    # 经验
                                    experience = com_post['experience']
                                    # 城市
                                    city = com_post['city']
                                    # 地方
                                    district = com_post['district']
                                    # 公司位置
                                    location = com_post['location']
                                    # 学历
                                    education = com_post['education']
                                    # 数量
                                    employerNumber = com_post['employerNumber']
                                    # 招聘来源
                                    source = com_post['source']
                                    # 工作职责
                                    description = com_post['description']
                                    # 发布时间
                                    startdate = com_post['startdate']
                                    if startdate:
                                        timeArray = time.localtime(startdate / 1000)
                                        startdate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                    else:
                                        startdate = None
                                    # 停止时间
                                    enddate = com_post['enddate']
                                    if enddate:
                                        timeArray = time.localtime(enddate / 1000)
                                        enddate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                    else:
                                        enddate = None
                                    # 详细招聘链接
                                    urlPath = com_post['urlPath']
                                    args = (com_name, title, oriSalary, experience, city, district, location, education,
                                            employerNumber, source, description, startdate, enddate, urlPath)
                                    self.insert_zhaopin(args)
                                print(f'招聘第{page}页插入成功！！！！')

    def insert_zhaopin(self, args):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = """insert into tp_zhaopin(com_name, title, oriSalary, experience, city, district, location, education, employerNumber, source, description, startdate, enddate, urlPath) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
        try:
            cursor = db.cursor()
            cursor.execute(sql, args)
            db.commit()
            cursor.close()
            db.close()
        except RequestException as err:
            print(err)

    def insert_wechat(self, item, main_id):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_wechat(c_id,title,publicNum,codeImg,titleImgURL,recommend) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['title'], item['publicNum'], item['codeImg'], item['titleImgURL'],
                item['recommend']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_judicialSale(self, cid, main_id):
        url = 'https://api9.tianyancha.com/services/v3/expanse/judicialSale?id={}&pageNum={}&pageSize=10'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            totalCount = data['count']
            if totalCount:
                totalpage = math.ceil(totalCount / 10)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(cid, i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['resultList']:
                            item = {}
                            # 标的名称
                            item['title'] = info['title']
                            # 法院
                            item['court'] = info['court']
                            # 公告时间
                            item['pubTime'] = info['pubTime']
                            # 起拍价
                            item['initial_price'] = None
                            # 评估价
                            item['consult_price'] = None
                            if info['detail']:
                                item['initial_price'] = info['detail'][0]['initial_price']
                                item['consult_price'] = info['detail'][0]['consult_price']
                            self.insert_judicialSale(item, main_id)

    def insert_judicialSale(self, item, main_id):
        print("插入司法拍卖信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_judicialSale(c_id,title,court,pubTime,initial_price,consult_price) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['title'], item['court'], item['pubTime'], item['initial_price'],
                item['consult_price']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_getPledgeReg(self, cid, main_id):
        url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getPledgeReg?cId={}&pageNum={}&pageSize=10'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            totalCount = data['totalCount']
            if totalCount:
                totalpage = math.ceil(totalCount / 10)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(cid, i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['list']:
                            item = {}
                            # 登记名称
                            item['iprName'] = info['iprName']
                            # 登记证号
                            item['iprCertificateNum'] = info['iprCertificateNum']
                            # 种类
                            item['iprType'] = info['iprType']
                            # 出质人名称
                            item['pledgorName'] = info['pledgorName']
                            # 质权人名称
                            item['pledgeeName'] = info['pledgeeName']
                            # 质权登记期限
                            item['pledgeRegPeriod'] = info['pledgeRegPeriod']
                            # 状态
                            item['state'] = info['state']
                            # 公示日期
                            item['publicityDate'] = info['publicityDate']
                            self.insert_PledgeReg(item, main_id)

    def insert_PledgeReg(self, item, main_id):
        print("插入知识产权出质信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_PledgeReg(c_id,iprName,iprCertificateNum,iprType,pledgorName,pledgeeName,pledgeRegPeriod,state,publicityDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['iprName'], item['iprCertificateNum'], item['iprType'], item['pledgorName'],
                item['pledgeeName'], item['pledgeRegPeriod'], item['state'], item['publicityDate']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_companyMortgage(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/ar/companyMortgageV2?name={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(quote(com_name), 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            count = data['count']
            if count:
                totalpage = math.ceil(count / 20)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(quote(com_name), i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['items']:
                            if info['baseInfo']:
                                print("get_companyMortgage baseInfo: ", info['baseInfo'])
                                item = {}
                                # 登记编号
                                item['regNum'] = self.ExistOrNot(info['baseInfo'], 'regNum')
                                # 登记日期
                                item['regDate'] = self.ExistOrNot(info['baseInfo'], 'regDate')
                                # 登记机关
                                item['regDepartment'] = self.ExistOrNot(info['baseInfo'], 'regDepartment')
                                # 被担保债权种类
                                item['warrantType'] = self.ExistOrNot(info['baseInfo'], 'type')
                                # 被担保债权数额
                                item['amount'] = self.ExistOrNot(info['baseInfo'], 'amount')
                                # 债务人履行债务期限
                                item['term'] = self.ExistOrNot(info['baseInfo'], 'term')
                                # 担保范围
                                item['scope'] = self.ExistOrNot(info['baseInfo'], 'scope')
                                # 备注
                                item['remark'] = self.ExistOrNot(info['baseInfo'], 'remark')
                                item['cancelReason'] = None
                                if info['cancelInfo']:
                                    item['cancelReason'] = info['cancelInfo']['cancelReason']
                                mortgage_main_id = self.insert_Main_Mortgage(item, main_id)
                                print(mortgage_main_id)
                                if info['changeInfoList']:
                                    for changeInfo in info['changeInfoList']:
                                        item = {}
                                        item['changeDate'] = changeInfo['changeDate']
                                        item['changeContent'] = changeInfo['changeContent']
                                        self.insert_Sub_Change_Mortgage(item, mortgage_main_id)
                                if info['peopleInfo']:
                                    for people in info['peopleInfo']:
                                        item = {}
                                        #
                                        item['licenseNum'] = people['licenseNum']
                                        # 抵押权人名称
                                        item['peopleName'] = people['peopleName']
                                        # 抵押权人证件类型
                                        item['liceseType'] = people['liceseType']
                                        self.insert_Sub_People_Mortgage(item, mortgage_main_id)

    def insert_Sub_People_Mortgage(self, item, mortgage_main_id):
        print("插入动产抵押信息抵押权人信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_sub_people_mortgage(m_id,licenseNum,peopleName,liceseType) values (%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                mortgage_main_id, item['licenseNum'], item['peopleName'], item['liceseType']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def insert_Sub_Change_Mortgage(self, item, mortgage_main_id):
        print("插入动产抵押信息变更信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_sub_change_mortgage(m_id,changeDate,changeContent) values (%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                mortgage_main_id, item['changeDate'], item['changeContent']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def insert_Main_Mortgage(self, item, main_id):
        print("插入动产抵押信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_Main_Mortgage(c_id,regNum,regDate,regDepartment,warrantType,amount,term,scope,remark,cancelReason) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['regNum'], item['regDate'], item['regDepartment'],
                item['warrantType'], item['amount'], item['term'], item['scope'], item['remark'], item['cancelReason']
            ))
            idS = db.insert_id()
            db.commit()
            db.close()
            return idS
        except RequestException as err:
            print(err)
            return None

    def get_companyEquity(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/ar/companyEquity?name={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(quote(com_name), 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            count = data['count']
            if count:
                totalpage = math.ceil(count / 20)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(quote(com_name), i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['items']:
                            item = {}
                            # 登记编号
                            item['regNumber'] = info['regNumber']
                            # 状态
                            item['state'] = info['state']
                            # 出质人
                            item['pledgor'] = info['pledgor']
                            # 出质人证件号
                            item['certifNumberR'] = info['certifNumberR']
                            # 出质股权数
                            item['equityAmount'] = info['equityAmount']

                            item['cancelReason'] = None
                            if 'cancel' in info:
                                item['cancelReason'] = info['cancel']
                            item['cancelDate'] = None
                            if 'cancelDate' in info:
                                item['cancelDate'] = info['cancelDate']
                            # 质权人
                            item['pledgee'] = info['pledgee']
                            # 质权人证件号
                            item['certifNumber'] = info['certifNumber']
                            # 股权出质登记日期
                            item['regDate'] = info['regDate']
                            self.insert_companyEquity(item, main_id)

    def insert_companyEquity(self, item, main_id):
        print("插入股权出质信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_companyEquity(c_id,regNumber,state,pledgor,certifNumberR,equityAmount,cancelReason,cancelDate,pledgee,certifNumber,regDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['regNumber'], item['state'], item['pledgor'],
                item['certifNumberR'], item['equityAmount'], item['cancelReason'], item['cancelDate'], item['pledgee'],
                item['certifNumber'], item['regDate']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_illegal(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/ar/Illegal?name={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(quote(com_name), 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            count = data['count']
            if count:
                totalpage = math.ceil(count / 20)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(quote(com_name), i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['items']:
                            item = {}
                            # 列入原因
                            item['putReason'] = info['putReason']
                            # 列入决定机关
                            item['putDepartment'] = info['putDepartment']
                            # 列入日期
                            item['putDate'] = info['putDate']
                            # 移除原因
                            item['removeReason'] = info['removeReason']
                            # 移除机关
                            item['removeDepartment'] = info['removeDepartment']
                            item['removeDate'] = None
                            self.insert_illegal(item, main_id)

    def insert_illegal(self, item, main_id):
        print("插入严重违法信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_illegal(c_id,putReason,putDepartment,putDate,removeReason,removeDepartment,removeDate) values (%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['putReason'], item['putDepartment'], item['putDate'],
                item['removeReason'], item['removeDepartment'], item['removeDate']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_punishment(self, cid, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getCreditChina?cId={}&pageNum={}&pageSize=20'
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            totalCount = data['totalCount']
            if totalCount:
                totalpage = math.ceil(totalCount / 20)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(cid, i), self.post_headers)
                    json_data = json.loads(html)
                    data = json_data['data']
                    if data:
                        for info in data['list']:
                            item = {}
                            # 处罚名称
                            item['punishName'] = info['punishName']
                            # 决定文书号
                            item['punishNumber'] = info['punishNumber']
                            # 处罚事由
                            item['reason'] = info['reason']
                            # 处罚状态
                            item['punishStatus'] = info['punishStatus']
                            # 处罚决定日期
                            item['decisionDate'] = info['decisionDate']
                            # 处罚类别1
                            item['punishType'] = info['type']
                            # 处罚类别2
                            item['punishTypeSecond'] = info['typeSecond']
                            # 处罚依据
                            item['evidence'] = info['evidence']
                            # 处罚结果
                            item['result'] = info['result']
                            # 处罚机关
                            item['departmentName'] = info['departmentName']
                            self.insert_punishment(item, main_id)
        AIC_url = 'https://api9.tianyancha.com/services/v3/ar/punishment?name={}&pageNum={}&pageSize=20'
        print("获取行政处罚信息")
        print(quote(com_name))
        AIC_html = self.get_index_html(AIC_url.format(quote(com_name), 1), self.post_headers)
        AIC_json_data = json.loads(AIC_html)
        AIC_data = AIC_json_data['data']
        if AIC_data:
            count = AIC_data['count']
            if count:
                totalpage = math.ceil(count / 20)
                for i in range(1, totalpage + 1):
                    AIC_html = self.get_index_html(AIC_url.format(quote(com_name), i), self.post_headers)
                    AIC_json_data = json.loads(AIC_html)
                    AIC_data = AIC_json_data['data']
                    if AIC_data:
                        for info in AIC_data['items']:
                            item = {}
                            # 处罚名称
                            item['punishName'] = None
                            # 决定文书号
                            item['punishNumber'] = info['punishNumber']
                            # 处罚状态
                            item['punishStatus'] = None
                            # 处罚决定日期
                            item['decisionDate'] = info['decisionDate']
                            # 处罚机关
                            item['departmentName'] = info['departmentName']
                            # 处罚类别1
                            item['punishType'] = None
                            # 处罚类别2
                            item['punishTypeSecond'] = None
                            # 处罚事由.类型
                            item['reason'] = info['type']
                            # 处罚依据
                            item['evidence'] = None
                            # 处罚结果
                            item['result'] = info['content']
                            self.insert_punishment(item, main_id)

    def insert_punishment(self, item, main_id):
        print("插入行政处罚信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_punishment(c_id,punishName,punishNumber,reason,punishStatus,decisionDate,punishType,punishTypeSecond,evidence,result,departmentName) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['punishName'], item['punishNumber'], item['reason'],
                item['punishStatus'], item['decisionDate'], item['punishType'], item['punishTypeSecond'],
                item['evidence'], item['result'], item['departmentName']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_judicial(self, cid, main_id):
        url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getJudicialList?cId={}&pageSize=20&pageNum={}'
        print("获取司法协助信息")
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            totalCount = data['totalCount']
            totalpage = math.ceil(totalCount / 20)
            idList = []
            for i in range(1, totalpage + 1):
                html = self.get_index_html(url.format(cid, i), self.post_headers)
                json_data = json.loads(html)
                data = json_data['data']
                if data:
                    for info in data['list']:
                        idList.append(info['assId'])
            self.get_detail_judicial(idList, main_id)

    def get_detail_judicial(self, idList, main_id):
        print(idList)
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        for idl in idList:
            url = 'https://api9.tianyancha.com/services/v3/aboutCompany/getJudicialDetail?assId={}'
            # print("获取执行人信息")
            html = self.get_index_html(url.format(idl), self.post_headers)
            json_data = json.loads(html)
            data = json_data['data']
            print(data)
            if data:
                if data['removeFrozen']:
                    item = {}
                    # 执行法院
                    try:
                        item['executiveCourt'] = data['removeFrozen']['executiveCourt']
                    except:
                        item['executiveCourt'] = ''
                    # 执行事项
                    try:
                        item['implementationMatters'] = data['removeFrozen']['implementationMatters']
                    except:
                        item['implementationMatters'] = ''
                    # 执行裁定文书号
                    try:
                        item['executeOrderNum'] = data['removeFrozen']['executeOrderNum']
                    except:
                        item['executeOrderNum'] = ''
                    # 执行通知文书号
                    try:
                        item['executeNoticeNum'] = data['removeFrozen']['executeNoticeNum']
                    except:
                        item['executeNoticeNum'] = ''
                    # 被执行人
                    try:
                        item['executedPerson'] = data['removeFrozen']['executedPerson']
                    except:
                        item['executedPerson'] = ''
                    # 被执行人持有股权与其他
                    try:
                        item['equityAmountOther'] = data['removeFrozen']['equityAmountOther']
                    except:
                        item['equityAmountOther'] = ''
                    # 被执行人证照种类
                    try:
                        item['licenseType'] = data['removeFrozen']['licenseType']
                    except:
                        item['licenseType'] = ''
                    # 被执行人证照号码
                    try:
                        item['licenseNum'] = data['removeFrozen']['licenseNum']
                    except:
                        item['licenseNum'] = ''
                    # 冻结期限自
                    try:
                        item['fromDate'] = data['removeFrozen']['fromDate']
                    except:
                        item['fromDate'] = ''
                    # 冻结期限至
                    try:
                        item['toDate'] = data['removeFrozen']['toDate']
                    except:
                        item['toDate'] = ''
                    # 冻结期限
                    try:
                        item['period'] = data['removeFrozen']['period']
                    except:
                        item['period'] = ''
                    # 公示日期
                    try:
                        item['publicityAate'] = data['removeFrozen']['publicityAate']
                    except:
                        item['publicityAate'] = ''
                    print(item)
                    self.insert_judicial(item, main_id)

    def insert_judicial(self, item, main_id):
        print("插入司法协助信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_judicial(c_id,executiveCourt,implementationMatters,executeOrderNum,executeNoticeNum,executedPerson,equityAmountOther,licenseType,licenseNum,fromDate,toDate,period,publicityAate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['executiveCourt'], item['implementationMatters'], item['executeOrderNum'],
                item['executeNoticeNum'], item['executedPerson'], item['equityAmountOther'], item['licenseType'],
                item['licenseNum'], item['fromDate'], item['toDate'],
                item['period'], item['publicityAate']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_zhixing(self, cid, main_id):
        url = 'https://api9.tianyancha.com/services/v3/ar/zhixing?id={}&pageNum={}&pageSize=20'
        print("获取执行人信息")
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(cid, 1), self.post_headers)
        json_data = json.loads(html)
        data = json_data['data']
        if data:
            count = data['count']
            totalpage = math.ceil(count / 20)
            for i in range(1, totalpage + 1):
                html = self.get_index_html(url.format(cid, i), self.post_headers)
                json_data = json.loads(html)
                get_data = json_data['data']
                if get_data:
                    for items in get_data['items']:
                        item = {}
                        # 被执行人
                        item['pname'] = items['pname']
                        # 组织机构代码
                        item['partyCardNum'] = items['partyCardNum']
                        # 执行标的
                        item['execMoney'] = items['execMoney']
                        # 执行法院
                        item['execCourtName'] = items['execCourtName']
                        # 立案时间
                        item['caseCreateTime'] = items['caseCreateTime']
                        # 案号
                        item['caseCode'] = items['caseCode']
                        self.insert_zhixing(item, main_id)

    def insert_zhixing(self, item, main_id):
        print("插入执行人信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_zhixing(c_id,pname,partyCardNum,execMoney,execCourtName,caseCreateTime,caseCode) values (%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['pname'], item['partyCardNum'], item['execMoney'], item['execCourtName'],
                item['caseCreateTime'], item['caseCode']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_dishonest(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/t/dishonest/app?keyWords={}&pageNum={}'
        print("获取失信信息")
        if 'Content-Length' in self.post_headers:
            self.post_headers.pop('Content-Length')
        html = self.get_index_html(url.format(quote(com_name), 1), self.post_headers)
        json_data = json.loads(html)
        if json_data['state'] == 'ok':
            data = json_data['data']
            if data:
                total = data['total']
                pageSize = data['pageSize']
                totalpage = math.ceil(total / pageSize)
                for i in range(1, totalpage + 1):
                    html = self.get_index_html(url.format(quote(com_name), i), self.post_headers)
                    json_data = json.loads(html)
                    if json_data['state'] == 'ok':
                        get_data = json_data['data']
                        if get_data:
                            for items in get_data['items']:
                                item = {}
                                item['iname'] = items['iname']
                                # 组织机构代码/身份证号
                                item['cardnum'] = items['cardnum']
                                # 地区
                                item['areaname'] = items['areaname']
                                # 立案时间
                                item['regdate'] = items['regdate']
                                # 发布时间
                                item['publishdate'] = items['publishdate']
                                # 执行依据单位
                                item['gistunit'] = items['gistunit']
                                # 执行法院
                                item['courtname'] = items['courtname']
                                # 执行依据文号
                                item['gistid'] = items['gistid']
                                # 案号
                                item['casecode'] = items['casecode']
                                # 法律生效文书确定的义务
                                item['duty'] = items['duty']
                                # 被执行人的履行情况
                                item['performance'] = items['performance']
                                # 失信被执行人行为具体情形
                                item['disrupttypename'] = items['disrupttypename']
                                self.insert_dishonest(item, main_id)

    def insert_dishonest(self, item, main_id):
        print("插入失信公司信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_dishonest(c_id,iname,cardnum,areaname,regdate,publishdate,gistunit,courtname,gistid,casecode,duty,performance,disrupttypename) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['iname'], item['cardnum'], item['areaname'], item['regdate'],
                item['publishdate'], item['gistunit'], item['courtname'], item['gistid'], item['casecode'],
                item['duty'], item['performance'], item['disrupttypename']

            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_court(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/t/court/{}?pageNum={}&pageSize=50'
        print("获取法院公告信息")
        # print(quote(com_name))
        try:
            if 'Content-Length' in self.post_headers:
                self.post_headers.pop('Content-Length')
            # print(self.post_headers)
            html = self.get_index_html(url.format(quote(com_name), 1), self.post_headers)
            json_data = json.loads(html)
            if json_data['state'] == 'ok':
                total = json_data['total']
                if total:
                    totalpage = math.ceil(total / 50)
                    for i in range(1, totalpage + 1):
                        html = self.get_index_html(url.format(quote(com_name), i), self.post_headers)
                        json_data = json.loads(html)
                        if json_data['state'] == 'ok':
                            if json_data['courtAnnouncements']:
                                for courtAnnouncements in json_data['courtAnnouncements']:
                                    item = {}
                                    # 当事人
                                    item['party'] = courtAnnouncements['party2']
                                    # 公告类型
                                    item['AnnounceType'] = courtAnnouncements['bltntypename']
                                    item['publishdate'] = courtAnnouncements['publishdate']
                                    # 刊登版面
                                    item['publishpage'] = courtAnnouncements['publishpage']
                                    # 上述方
                                    item['appellant'] = courtAnnouncements['party1']
                                    item['courtcode'] = courtAnnouncements['courtcode']

                                    item['content'] = courtAnnouncements['content']
                                    item['province'] = courtAnnouncements['province']
                                    self.insert_court(item, main_id)
        except Exception as e:
            print(f'出错了{e}')

    def insert_court(self, item, main_id):
        print("插入法院公告信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_court(c_id,party,AnnounceType,publishdate,publishpage,appellant,courtcode,content,province) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['party'], item['AnnounceType'], item['publishdate'], item['publishpage'],
                item['appellant'], item['courtcode'],
                item['content'], item['province']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_lawsuit(self, com_name, main_id):
        url = 'https://api9.tianyancha.com/services/v3/t/lawsuitscr'
        # print(self.headers)
        # print(self.paramdata)
        html = self.post_index_html(url, com_name)
        data = json.loads(html)
        # print("")
        print("get_lawsuit: ", data)
        if data['state'] == 'warn':
            print('无数据')
        elif "total" in data['data']:
            print("data['data']: ", data['data'])
            total = data['data']['total']
            totalpage = math.ceil(total / 20)
            lawsuitUrlList = []
            for i in range(1, totalpage + 1):
                self.paramdata.update({'pn': i})
                html = self.post_index_html(url, com_name)
                data = json.loads(html)
                if data['data']:
                    for items in data['data']['items']:
                        lawsuitUrlList.append(items['lawsuitUrl'])
            self.parse_detal_lawsuit(lawsuitUrlList, com_name, main_id)
        # print(html)

    def parse_detal_lawsuit(self, lawsuitUrlList, com_name, main_id):
        for lawurl in lawsuitUrlList:
            url = lawurl + "?version=TYC-XCX-WX&auth={}&authToken=&sharecode=undefined".format(
                self.headers.get('authorization'))
            # print(url)
            html = self.get_lawsuit_html(url)
            # print(html)
            elem = etree.HTML(html)
            htmlString = ''.join(elem.xpath("//div[@class='lawsuitcontent']/div/div/text()"))
            item = {}
            item['com_name'] = com_name
            item['lawsuit'] = htmlString
            self.insert_lawsuit(item, main_id)
            # for i in range(len(htmlString)):
            #     plaintiff = re.findall('原告:(.*)', htmlString[i])
            #     if plaintiff:
            #         item['plaintiff'] = plaintiff[0]
            # for htmll in htmlString:
            #     htmll = str(htmll)
            #     htmll = htmll.encode('utf-8').decode('utf-8')
            #     print(htmll)
            #     print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")
            #     plaintiff = re.findall('原告:(.*)', htmll)
            #     if plaintiff:
            #         print("/////////////////////////////////////")
            #         print(plaintiff)
            #         # item['plaintiff'] = plaintiff[0]
            # print(item)
            # print((htmlString))
            # s2 = re.sub(r'<.*?>', '', htmlString)
            # tml=HTMLParser().unescape(s2)
            # print(tml)

    def insert_lawsuit(self, item, main_id):
        print("插入法律诉讼信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_lawsuit(c_id,com_name,lawsuit) values (%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['com_name'], item['lawsuit']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_announcement(self, cid, main_id):
        print("获取开庭公告信息")
        url = 'https://api9.tianyancha.com/services/v3/expanse/announcement?id={}&pageNum={}&pageSize=20'
        html = self.get_index_html(url.format(cid, 1), self.headers)
        data = json.loads(html)
        if data['data']:
            count = data['data']['count']
            totalpage = math.ceil(count / 20)
            for i in range(1, totalpage + 1):
                html = self.get_index_html(url.format(cid, i), self.headers)
                use_data = json.loads(html)
                if use_data['data']['resultList']:
                    for result in use_data['data']['resultList']:
                        item = {}
                        # 开庭日期
                        item['startDate'] = self.ExistOrNot(result, 'startDate')
                        # 案由
                        item['caseReason'] = self.ExistOrNot(result, 'caseReason')
                        # 案号
                        item['caseNo'] = self.ExistOrNot(result, 'caseNo')
                        # 当事人
                        item['litigant'] = self.ExistOrNot(result, 'litigant')
                        # 原告
                        item['plaintiff'] = ''
                        if result['plaintiff']:
                            for plaintiff in result['plaintiff']:
                                item['plaintiff'] = item['plaintiff'] + plaintiff['name'] + '、'
                        # 被告
                        item['defendant'] = ''
                        if result['defendant']:
                            for defendant in result['defendant']:
                                item['defendant'] = item['defendant'] + defendant['name'] + '、'
                        # 法院
                        item['court'] = self.ExistOrNot(result, 'court')
                        # 法庭
                        item['courtroom'] = self.ExistOrNot(result, 'courtroom')
                        self.insert_announcement(item, main_id)
                # 每次解析睡眠2秒
                time.sleep(2)

    def insert_announcement(self, item, main_id):
        print("插入开庭公告信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_announcement(c_id,startDate,caseReason,caseNo,litigant,plaintiff,defendant,court,courtroom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['startDate'], item['caseReason'], item['caseNo'], item['litigant'],
                item['plaintiff'], item['defendant'], item['court'], item['courtroom']
            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_invest(self, cid, main_id):
        url = 'https://api9.tianyancha.com/services/v3/expanse/inverstV2?id={}&pageNum={}&pageSize=20'
        html = self.get_index_html(url.format(cid, 1), self.headers)
        data = json.loads(html)
        if data['data']:
            total = data['data']['total']
            totalpage = math.ceil(total / 20)
            for i in range(1, totalpage + 1):
                html = self.get_index_html(url.format(cid, i), self.headers)
                use_data = json.loads(html)
                if use_data['data']['result']:
                    for result in use_data['data']['result']:
                        item = {}
                        item['com_name'] = result['name']
                        # 投资数额
                        item['invest_amount'] = result['amount']
                        # 投资占比
                        item['invest_percent'] = result['percent']
                        # 公司类型
                        item['orgType'] = result['orgType']
                        # 经营范围
                        item['business_scope'] = result['business_scope']
                        # 状态
                        item['regStatus'] = result['regStatus']
                        # 合伙人
                        item['alias'] = result['alias']
                        # 成立时间
                        item['estiblishTime'] = result['estiblishTime']
                        # 法人
                        item['legalPersonName'] = result['legalPersonName']
                        # 行业
                        item['category'] = result['category']
                        # 注册资本
                        item['regCapital'] = result['regCapital']
                        # 社会统一代码
                        item['creditCode'] = self.ExistOrNot(result, 'creditCode')
                        self.insert_invest(item, main_id)

    def insert_invest(self, item, main_id):
        print("插入投资信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_invest(c_id,com_name,invest_amount,invest_percent,orgType,business_scope,regStatus,alias,estiblishTime,legalPersonName,category,regCapital,creditCode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['com_name'], item['invest_amount'], item['invest_percent'], item['orgType'],
                item['business_scope'], item['regStatus'], item['alias'], item['estiblishTime'],
                item['legalPersonName'], item['category'], item['regCapital'], item['creditCode']

            ))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_change(self, comChanInfoList, main_id):
        print("搜索变更信息")
        if comChanInfoList:
            for change in comChanInfoList:
                item = {}
                # 变更事项
                item['changeItem'] = change['changeItem']
                # 变更前
                item['contentBefore'] = change['contentBefore']
                # 变更后
                item['contentAfter'] = change['contentAfter']
                # 变更时间
                item['changeTime'] = change['changeTime']
                self.insert_change(item, main_id)

    def insert_change(self, item, main_id):
        print("插入分支机构信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_change(c_id,changeItem,contentBefore,contentAfter,changeTime) values (%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                main_id, item['changeItem'], item['contentBefore'], item['contentAfter'], item['changeTime']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_staff(self, staffList, main_id):
        print("搜索主要人员信息")
        if staffList:
            for staff in staffList:
                item = {}
                item['name'] = staff['name']
                item['position'] = ''
                try:
                    for i in range(len(staff['typeJoin'])):
                        item['position'] = item['position'] + staff['typeJoin'][i] + ","
                except:
                    pass
                print(item)
                self.insert_staff(item, main_id)

    def insert_staff(self, item, main_id):
        print("插入分支机构信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_staff(c_id,staff_name,staff_position) values (%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id,
                                 item['name'], item['position']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_branch(self, branchList, main_id):
        print("搜索分支机构信息")
        if branchList:
            for branch in branchList:
                item = {}
                item['name'] = self.ExistOrNot(branch, 'name')
                item['legalPersonName'] = self.ExistOrNot(branch, 'legalPersonName')
                item['category'] = self.ExistOrNot(branch, 'category')
                item['estiblishTime'] = self.ExistOrNot(branch, 'estiblishTime')
                item['regStatus'] = self.ExistOrNot(branch, 'regStatus')
                item['ty_comId'] = self.ExistOrNot(branch, 'id')
                self.insert_branch(item, main_id)

    def insert_branch(self, item, main_id):
        print("插入分支机构信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_branch(c_id,com_name,legalPersonName,category,estiblishTime,regStatus,ty_comId) values (%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id,
                                 item['name'], item['legalPersonName'], item['category'], item['estiblishTime'],
                                 item['regStatus'],
                                 item['ty_comId']))
            # print(sql)
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def get_holder(self, holder_list, main_id):
        print("获取股东信息")
        print(holder_list)
        if holder_list:
            for holder in holder_list:
                item = {}
                item['name'] = holder['name']
                item['tag'] = ''
                try:
                    for tag in holder['tagList']:
                        item['tag'] = item['tag'] + tag['name'] + "、"
                except:
                    item['tag'] = ''
                item['amomon'] = ''
                item['time'] = ''
                item['percent'] = ''
                item['paymet'] = ''
                if holder['capital']:
                    item['amomon'] = self.ExistOrNot(holder['capital'][0], "amomon")
                    item['time'] = self.ExistOrNot(holder['capital'][0], "time")
                    item['percent'] = self.ExistOrNot(holder['capital'][0], "percent")
                    item['paymet'] = self.ExistOrNot(holder['capital'][0], "paymet")
                print(item)
                self.insert_holder(item, main_id)

    def insert_holder(self, item, main_id):
        print("插入股东信息")
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into tp_holder(c_id,person_name,tag,amomon,h_time,percent,paymet) values (%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (main_id,
                                 item['name'], item['tag'], item['amomon'], item['time'], item['percent'],
                                 item['paymet']))
            # print(sql)
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def ExistOrNot(self, jsonObj, key1, key2="_o_"):
        if key1 in jsonObj:
            if jsonObj[key1] == "-":
                return jsonObj[key1].replace("-", "")
            else:
                return jsonObj[key1]
        else:
            if key2 in jsonObj:
                if jsonObj[key2] == "-":
                    return jsonObj[key2].replace("-", "")
                else:
                    return jsonObj[key2]
            else:
                return None

    def insert_date(self, item):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into tp_com(com_name,legalPersonName,estiblishTime,regNumber,regCapital,actualCapital,creditCode,taxNumber,orgNumber,EName,regStatus,staffNumRange,socialStaffNum,companyOrgType,industry,fromTime,regLocation,approvedTime,regInstitute,businessScope,phoneNumber,email,baseInfo,local_update_time,ty_update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                item['com_name'], item['legalPersonName'], item['estiblishTime'], item['regNumber'], item['regCapital'],
                item['actualCapital'], item['creditCode'],
                item['taxNumber'], item['orgNumber'], item['EName'], item['regStatus'], item['staffNumRange'],
                item['socialStaffNum'], item['companyOrgType'],
                item['industry'], item['fromTime'], item['regLocation'], item['approvedTime'], item['regInstitute'],
                item['businessScope'], item['phoneNumber'], item['email'], item['baseInfo'], uptime,
                item['ty_update_time']
            ))
            # print(sql)
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    @retry(stop_max_attempt_number=100)
    def get_index_html(self, url, headers):
        try:
            response = requests.get(url, headers=headers, proxies=self.proxy, timeout=5, verify=False)
            print(response.status_code)
        except:
            self.set_Proxy_False()
        if response.status_code is not 200:
            print("响应非200,重新解析")
            print(url)
            self.set_Proxy_False()
        return response.text

    @retry(stop_max_attempt_number=100)
    def get_lawsuit_html(self, url):
        try:
            response = requests.get(url, headers=self.lawsuit_headers, proxies=self.proxy, timeout=5, verify=False)
        except:
            self.set_Proxy_False()
        print(response.status_code)
        if response.status_code is not 200:
            print("响应非200,重新解析")
            print(url)
            self.set_Proxy_False()
        return response.text

    @retry(stop_max_attempt_number=100)
    def post_tmInfo_html(self, url, id, page):
        self.paramdata.update(
            {"id": id, "pn": page, "int_cls": -100, "status": -100, "category": -100, "app_year": -100})
        self.post_headers.update({'Content-Length': '84'})
        print(self.paramdata)
        # print(self.post_headers)
        try:
            response = requests.post(url, headers=self.post_headers, proxies=self.proxy,
                                     data=json.dumps(self.paramdata), timeout=5, verify=False)
        except:
            self.set_Proxy_False()
        if response.status_code is not 200:
            print("响应非200,重新解析")
            print(url)
            self.set_Proxy_False()

        return response.text

    @retry(stop_max_attempt_number=100)
    def post_index_html(self, url, com_name):
        self.paramdata.update({'keyWords': com_name})
        self.post_headers.update({'Content-Length': '84'})
        print(self.paramdata)
        # print(self.post_headers)
        try:
            response = requests.post(url, headers=self.post_headers, proxies=self.proxy,
                                     data=json.dumps(self.paramdata), timeout=5, verify=False)
        except:
            self.set_Proxy_False()
        if response.status_code is not 200:
            print("响应非200,重新解析")
            print(url)
            self.set_Proxy_False()

        return response.text

    def set_Proxy_False(self):
        self.ss.setFalse(self.proxy['http'].split(":")[0], self.proxy['http'].split(":")[1], 'ty')
        self.ss.setFalse(self.proxy['https'].split(":")[0], self.proxy['https'].split(":")[1], 'ty')
        self.get_PROXY()
        raise Exception

    def get_bloomFilter(self, sql):
        bloom = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        db = pymysql.connect("192.168.1.68", "root", "password", "phtest", charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        desc = cursor.description
        object_dict = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        # print(object_dict)
        cursor.close()
        for d in object_dict:
            # print(d)
            bloom.add(d)
        return bloom

    def get_search_list(self):
        db = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
        sql = "select * from qiye where dustry like '%福建%'"
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rs = cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        return rs

    def select_main_id(self, sql):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        # sql = "select id from tp_com where com_name=%s"
        global idS
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            idS = cursor.fetchone()
            if idS:
                print(idS[0])
                idS = int(idS[0])
            db.commit()
            db.close()
        except:
            print("查询数据错误")
        return idS

    def ifInDatabase(self, sql):
        db = pymysql.connect("192.168.1.68", "root", "password", "phtest", charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        rs = cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        return rs


if __name__ == '__main__':
    t = Tphone("福建诚华信用管理")
    t.run()
