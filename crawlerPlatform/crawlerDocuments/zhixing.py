# coding=utf-8
import requests
from selenium import webdriver
from crawlerDocuments.yundama import identify
import time
import json
from fake_useragent import UserAgent
import re
import execjs
import random

from lxml import etree


class Zhi():

    def __init__(self, keyword):
        self.ua = UserAgent()
        # self.driver = webdriver.Firefox()
        self.cookies = {}
        self.keyword = keyword
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,es;q=0.9,es-ES;q=0.8,zh-CN;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '282',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'SESSIONID=5DA27ED12FB54362924085DD64FA169D; _gscu_1138507821=513398239m3ys865; UM_distinctid=1696ac78dccfb-009f7a2d6ee17d-9393265-100200-1696ac78dcf1fb; _gscbrs_1138507821=1; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1552354555,1552355100,1552355399,1552355839; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1552355839; _gscs_1138507821=t523545557henqk79|pv:60',
            'DNT': '1',
            'Host': 'zxgk.court.gov.cn',
            'Origin': 'http://zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhzxgk/',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,es;q=0.9,es-ES;q=0.8,zh-CN;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'JSESSIONID=83B333D76598E428E46BF5C2E613DDDB; _gscu_15322769=51339870oumown91; UM_distinctid=1696ac78dccfb-009f7a2d6ee17d-9393265-100200-1696ac78dcf1fb; SESSION=a17de62b-d441-4b18-bb9e-9cd9824c0f30; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1557969694; _gscbrs_15322769=1; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1557970706; _gscs_15322769=57969697oi5ok791|pv:4',
            'DNT': '1',
            'Host': 'zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhzxgk/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # self.searchCourtName = '全国法院（包含地方各级法院）'
        self.data = {
            # 'pName': '',
            'pCardNum': '',
            'selectCourtId': '0',
            # 'pCode': 'x9gb',
            # 'captchaId': 'KSBFIJoAKNqIFCKmRnoO4EoR80Ex5wM0',
            'searchCourtName': '全国法院（包含地方各级法院）',
            'selectCourtArrange': '1',
            'currentPage': '1'
        }
        self.key = ''

    def run(self):

        # url = "http://zxgk.court.gov.cn/zhzxgk/"
        # self.driver.get(url)
        # # self.key = input("公司名称: ")
        # self.driver.find_element_by_xpath('//*[@id="pName"]').send_keys('福建一建集团有限公司')
        flag = True
        while flag:
            url = 'http://zxgk.court.gov.cn/zhzxgk/captcha.do?captchaId={}&random={}'
            ra = random.random()
            captchaId = self.get_captchaId()
            url = url.format(str(captchaId), str(ra))
            print("url: ", url)
            content = requests.get(url).content
            with open("zhixing_new.jpg", 'wb') as f:
                f.write(content)
            code = identify(content)
            print("code: ", code)
            uurl = 'http://zxgk.court.gov.cn/zhzxgk/checkyzm?captchaId={}&pCode={}'
            uurl = uurl.format(str(captchaId), str(code))
            print("uurl: ", uurl)
            response = requests.get(uurl)
            print(response.text)
            print(type(response.text))
            if response.text.strip() == '1':
                flag = False

        #     print(self.driver.find_element_by_id('captchaId').get_attribute('value'))
        #
        #     self.driver.find_element_by_id('yzm').clear()
        #     self.driver.find_element_by_id('captchaImg').click()
        #     search_url = self.driver.find_element_by_id('captchaImg').get_attribute("src")
        #     print(search_url)
        #     content = requests.get(search_url).content
        #     with open("zhixing.jpg", 'wb') as f:
        #         f.write(content)
        #     code = identify(content)
        #     self.driver.find_element_by_id('yzm').send_keys(code)
        #     time.sleep(1)
        #     try:
        #         if self.driver.find_element_by_xpath("//div[@class='col-sm-2 alert alert-success mysetalert']"):
        #             flag = False
        #     except:
        #         print("验证出错")
        #
        # self.driver.find_element_by_xpath('//*[@id="yzm-group"]/div[6]/button').click()
        #
        # captchaId = self.driver.find_element_by_id('captchaId').get_attribute('value')
        #     验证结束,开始解析
        html = self.parse_index(captchaId, code,self.keyword)

        # print(html)
        json_data = json.loads(html)
        print('json数据')
        print(json_data)
        if json_data[0]['totalPage'] is not None:
            print('总页数')
            print(json_data[0]['totalPage'])
            id_list = []
            for i in range(1, int(json_data[0]['totalPage']) + 1):
                self.data.update({'currentPage': i})
                url = 'http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do'
                html = self.get_post_json(url)
                print(html)
                json_data = json.loads(html)
                for j in range(len(json_data[0]['result'])):
                    iter_data = {}
                    iter_data['caseCode'] = json_data[0]['result'][j]['caseCode']
                    iter_data['pname'] = json_data[0]['result'][j]['pname']
                    id_list.append(iter_data)

            print(id_list)
            if len(id_list):
                for ids in id_list:
                    # url = 'http://zxgk.court.gov.cn/zhzxgk/newdetail?id={}&j_captcha={}&captchaId={}'
                    url = 'http://zxgk.court.gov.cn/zhzxgk/detailZhcx.do?pnameNewDel={}&cardNumNewDel=&j_captchaNewDel={}&caseCodeNewDel={}&captchaIdNewDel={}'
                    url = url.format(ids['pname'], code, ids['caseCode'], captchaId)
                    print("详细url")
                    print(url)
                    detail_data = self.parse_detal(url)
                    # print(detail_data)
                    self.get_item(detail_data)

    def get_item(self, html):
        # 被执行人文书
        execute = re.findall('<div.*?>被执行人</div>([\s\S]*)</div>', html)
        if execute:
            print('被执行人')
            item = {}
            item['document_type'] = '被执行人'
            referenceNum = re.findall('''<strong>案号：</strong></td>\s*<td.*?>(.*?)</td>''', execute[0])
            # print(referenceNum)
            item['referenceNum'] = referenceNum[0] if referenceNum else None
            partyCardNum = re.findall('<strong>身份证号码/组织机构代码：</strong></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['partyCardNum'] = partyCardNum[0] if partyCardNum else None
            pname = re.findall('<strong>被执行人姓名/名称：</strong><br/></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['pname'] = pname[0] if pname else None
            execCourtName = re.findall('<strong>执行法院：</strong></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['execCourtName'] = execCourtName[0] if execCourtName else None
            caseCreateTime = re.findall('<strong>立案时间：</strong></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['caseCreateTime'] = caseCreateTime[0] if caseCreateTime else None
            sex = re.findall('<strong>性别：</strong></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['sex'] = sex[0] if sex else None
            execMoney = re.findall('<strong>执行标的：</strong></td>\s*<td.*?>(.*?)</td>', execute[0])
            item['execMoney'] = execMoney[0] if execMoney else None
            item['legalPerson'] = None
            item['province'] = None
            item['gistId'] = None
            item['gistUnit'] = None
            item['dutyDetail'] = None
            item['performance'] = None
            item['disruptTypeName'] = None
            item['publishDate'] = None
            item['endDate'] = None
            item['unexectued'] = None
            print(item)
        # 失信被执行人文书
        dishonest = re.findall('<div.*?>失信被执行人</div>([\s\S]*)</div>', html)
        if dishonest:
            print('失信被执行人')
            item = {}
            item['document_type'] = '失信被执行人'
            referenceNum = re.findall('''<strong>案号：</strong></td>\s*<td.*?>(.*?)</td>''', dishonest[0])
            # print(referenceNum)
            item['referenceNum'] = referenceNum[0] if referenceNum else None
            partyCardNum = re.findall('<strong>身份证号码/组织机构代码：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['partyCardNum'] = partyCardNum[0] if partyCardNum else None
            pname = re.findall('<strong>被执行人姓名/名称：</strong><br/></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['pname'] = pname[0] if pname else None
            execCourtName = re.findall('<strong>执行法院：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['execCourtName'] = execCourtName[0] if execCourtName else None
            caseCreateTime = re.findall('<strong>立案时间：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['caseCreateTime'] = caseCreateTime[0] if caseCreateTime else None
            item['sex'] = None
            execMoney = re.findall('<strong>执行标的：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['execMoney'] = execMoney[0] if execMoney else None
            legalPerson = re.findall('<strong>法定代表人或者负责人姓名：</strong></td>\s*<td.*?>(.*?)</td', dishonest[0])
            item['legalPerson'] = legalPerson[0] if legalPerson else None
            province = re.findall('<strong>省份：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['province'] = province[0] if province else None
            gistId = re.findall('<strong>执行依据文号：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['gistId'] = gistId[0] if gistId else None
            gistUnit = re.findall('<strong>做出执行依据单位：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['gistUnit'] = gistUnit[0] if gistUnit else None
            dutyDetail = re.findall('<strong>生效法律文书确定的义务：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['dutyDetail'] = dutyDetail[0] if dutyDetail else None
            performance = re.findall('<strong>被执行人的履行情况：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['performance'] = performance[0] if performance else None
            disruptTypeName = re.findall('<strong>失信被执行人行为具体情形：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['disruptTypeName'] = disruptTypeName[0] if disruptTypeName else None
            publishDate = re.findall('<strong>发布时间：</strong></td>\s*<td.*?>(.*?)</td>', dishonest[0])
            item['publishDate'] = publishDate[0] if publishDate else None
            item['endDate'] = None
            item['unexectued'] = None
            print(item)
        Final_case = re.findall('<div.*?>终本案件</div>([\s\S]*)</div>', html)
        if Final_case:
            print('终本案件')
            item = {}
            item['document_type'] = '终本案件'
            referenceNum = re.findall('''<strong>案号：</strong></td>\s*<td.*?>(.*?)</td>''', Final_case[0])
            # print(referenceNum)
            item['referenceNum'] = referenceNum[0] if referenceNum else None
            partyCardNum = re.findall('<strong>身份证号码/组织机构代码：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['partyCardNum'] = partyCardNum[0] if partyCardNum else None
            pname = re.findall('<strong>被执行人姓名/名称：</strong><br/></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['pname'] = pname[0] if pname else None
            execCourtName = re.findall('<strong>执行法院：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['execCourtName'] = execCourtName[0] if execCourtName else None
            caseCreateTime = re.findall('<strong>立案时间：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['caseCreateTime'] = caseCreateTime[0] if caseCreateTime else None
            execMoney = re.findall('<strong>执行标的：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['execMoney'] = execMoney[0] if execMoney else None
            endDate = re.findall('<strong>终本日期：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['endDate'] = endDate[0] if endDate else None
            unexectued = re.findall('<strong>未履行金额：</strong></td>\s*<td.*?>(.*?)</td>', Final_case[0])
            item['unexectued'] = unexectued[0] if unexectued else None
            item['legalPerson'] = None
            item['province'] = None
            item['gistId'] = None
            item['gistUnit'] = None
            item['dutyDetail'] = None
            item['performance'] = None
            item['disruptTypeName'] = None
            item['publishDate'] = None
            item['sex'] = None
            print(item)

    def parse_detal(self, url):
        response = requests.get(url, headers=self.headers2)
        html = response.text
        print(response.status_code)
        # print(html)
        # return json.loads(html)
        return html

    def parse_index(self, captchaId, code, keyword):
        self.data.update({'pName': keyword})
        self.data.update({'pCode': code})
        self.data.update({'captchaId': captchaId})
        # self.headers.update({'User-Agent': self.ua.random})
        url = 'http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do'
        # 'http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do'
        print(self.data)
        print(self.headers)
        html = self.get_post_json(url)
        return html

    def get_post_json(self, url):
        # self.refresh_cookies(self.driver.get_cookies())
        print(self.cookies)
        response = requests.post(url, headers=self.headers, data=self.data, cookies=self.cookies)
        print("*********************")
        print(response.status_code)
        return response.text

    # def get_code(self):
    # 刷新cookies
    def refresh_cookies(self, cookies):
        for cookie in cookies:
            self.cookies[cookie['name']] = cookie['value']

    def get_captchaId(self, ):
        ctx = execjs.compile('''
        function getNum() {
                var chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                        'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                        'x', 'y', 'z' ];
                var nums = "";
                for (var i = 0; i < 32; i++) {
                    var id = parseInt(Math.random() * 61);
                    nums += chars[id];
                }
                return nums;
            }

        ''')
        num = ctx.call("getNum")
        print(num)
        return num


if __name__ == '__main__':
    z = Zhi("福州")
    z.run()
