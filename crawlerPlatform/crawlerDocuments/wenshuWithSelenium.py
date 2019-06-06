from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from SetProxy import Ss
import requests
from retrying import retry
import traceback


class wenshu:
    def __init__(self, keyword):
        self.ss = Ss()
        # self.driver = webdriver.Chrome()
        self.keyword = keyword
        self.flag = True
        # self.driver.get("http://wenshu.court.gov.cn/")
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,es;q=0.9,es-ES;q=0.8,zh-CN;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': '_gscu_2116842793=52273440ywnq7o10; UM_distinctid=1696ac78dccfb-009f7a2d6ee17d-9393265-100200-1696ac78dcf1fb; _gscu_125736681=57995864bzltqo42; Hm_lvt_9e03c161142422698f5b0d82bf699727=1557995866; _gscbrs_2116842793=1; ASP.NET_SessionId=icwhpiao0wof52z2my2qjybm; VCode=9d22dc63-4209-42cd-9e08-4d10f9853748; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1557906014,1558659736,1558685673,1558686422; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1558686422; _gscs_2116842793=t58685672v35kdc86|pv:2; wzws_cid=311a044ff039278b6b7ebead2a13c9a378244c2b6c884b1a9bac7188cd3a536b7641830325f4265e0a7d1ad460b929a6cbceae07afe25365f739926c3ab2e1ba',
            'DNT': '1',
            'Host': 'wenshu.court.gov.cn',
            'Referer': 'http://wenshu.court.gov.cn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

    @retry(stop_max_attempt_number=100)
    def get_proxy(self):
        # 获取代理
        json_p = self.ss.getOne('ty')
        host = str(json_p['ip'])
        port = str(json_p['port'])
        hostport = host + ':' + port
        print("try ip: ", hostport)
        try:
            requests.get('http://wenshu.court.gov.cn/', headers=self.headers, proxies={'http': hostport}, timeout=2)
            print("current ip: ", hostport)
            return "http://" + hostport
        except:
            print("ip does't work ,try again !!!")
            raise Exception

    def parse_index(self):
        wait = WebDriverWait(self.driver, 20)
        # 等待搜索加载
        try:
            wait.until(
                lambda x: x.find_element_by_xpath("//div[@id='resultList']//a"))

            length = len(self.driver.find_element_by_xpath("//div[@id='resultList']").find_elements_by_tag_name("a"))
            print(length)
            # 获取当前窗口句柄
            index_handle = self.driver.current_window_handle

            # 获取所有的结果链接,并打开连接
            for i in range(0, length):
                links = self.driver.find_element_by_xpath("//div[@id='resultList']").find_elements_by_tag_name("a")
                link = links[i]
                # if not ("_blank" in link.get_attribute("target") or "http" in link.get_attribute("href")):
                link.click()
                # self.driver.back()
                time.sleep(2.5)
            # 获取当前窗口句柄集合（列表类型）
            handles = self.driver.window_handles
            for handle in handles:
                if handle != index_handle:
                    self.driver.switch_to_window(handle)
                    self.open_pages_and_parse_detail()
                    self.driver.close()
            self.driver.switch_to_window(index_handle)
        except:
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            # result = wait.until(lambda x: x.find_element_by_xpath("//div[@id='resultList']"))
            result = self.driver.find_element_by_xpath("//div[@id='resultList']").get_attribute("textContent")
            print("result: ", result)
            if result == "无符合条件的数据...":
                self.flag = False
            else:
                self.driver.close()

    @retry(stop_max_attempt_number=100)
    def run(self):
        firefoxOptions = webdriver.FirefoxOptions()
        ip = self.get_proxy()
        print("ip ", ip)
        # 设置代理
        firefoxOptions.add_argument("--proxy-server=" + ip)
        # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
        self.driver = webdriver.Firefox(firefox_options=firefoxOptions)
        self.driver.get("http://httpbin.org/ip")
        # print(self.driver.page_source)
        self.driver.get("http://wenshu.court.gov.cn/")

        wait = WebDriverWait(self.driver, 20)
        try:
            input_link = wait.until(
                lambda x: x.find_element_by_xpath("//div[@class='head_search_middle']/input"))
        except Exception as e:
            print(e)
            self.driver.close()
        input_link.click()
        input_link.send_keys(self.keyword)
        search_button = wait.until(lambda x: x.find_element_by_xpath("//div[@class='head_search_rightfloat']/button"))
        search_button.click()
        # 解析第一页
        self.parse_index()
        if self.flag:
            next_page = self.driver.find_element_by_xpath("//a[@class='next']")
            next_page.click()
            # 解析第二页
            self.parse_index()

    def is_element_visible(self, timeout, element):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(element))
            flag = True
        except:
            flag = False
        return flag

    def open_pages_and_parse_detail(self):

        if self.is_element_visible(20, (By.XPATH, "//div[@id='DivContent']/div")):
            elem = etree.HTML(self.driver.page_source)
            item = {}
            title_list = elem.xpath("//div[@id='contentTitle']//text()")
            item['title'] = ''
            for title in title_list:
                item['title'] += str(title).replace(" ", "")
            content_list = elem.xpath("//div[@id='DivContent']//text()")

            content_div = elem.xpath("//div[@id='DivContent']/div")
            if " " in content_list:
                content_list.remove(" ")
            if "{C}" in content_list:
                content_list.remove("{C}")
            copy_list = content_list.copy()
            content_list.clear()

            for content in copy_list:
                content_list.append(content.replace(u'\u3000', u' '))

            print(content_list)
            print("***************************************************************")
            # if len(content_list)<=1:

            item['court'] = content_list[0]
            print("content_div num: ", len(content_div))
            if len(content_div) <= 1:
                item['document_type'] = None
                item['num'] = None

            else:
                item['document_type'] = content_list[1]
                item['num'] = content_list[2]

            item['Retrial_applicant'] = ''
            item['legal_representative'] = ''
            item['delegate'] = ''
            item['respondent'] = ''
            item['appellant'] = ''
            item['person_in_charge'] = ''
            item['chief_judge'] = ''
            item['judge'] = ''
            item['acting_judge'] = ''
            item['date'] = ''
            item['court_clerk'] = ''
            item['judge_assistant'] = ''
            item["content"] = ''
            for i in range(len(content_list)):
                temp1 = re.findall("^再审申请人（.*?）(.*)", content_list[i])
                if temp1:
                    item['Retrial_applicant'] += temp1[0] + " "
                temp2 = re.findall("^法定代表人(.*)", content_list[i])
                if temp2:
                    item['legal_representative'] += temp2[0] + " "
                temp3 = re.findall("代理人：(.*)", content_list[i])
                if temp3:
                    item['delegate'] += temp3[0] + " "
                temp4 = re.findall("^被申请人.*?:(.*)", content_list[i])
                if temp4:
                    item['respondent'] += temp4[0] + " "
                temp5 = re.findall("^二审上诉人（.*?）(.*)", content_list[i])
                if temp5:
                    item['appellant'] += temp5[0] + " "
                temp6 = re.findall("^负责人(.*)", content_list[i])
                if temp6:
                    item['person_in_charge'] += temp6[0] + " "
                temp7 = re.findall("审\s*判\s*长\s*(.*)", content_list[i])
                # print("temp7 : ",temp7)
                if temp7:
                    item['chief_judge'] += temp7[0] + " "
                temp8 = re.findall("^审\s*判\s*员(.*)", content_list[i])
                if temp8:
                    item['judge'] += temp8[0] + " "
                temp9 = re.findall("^代理审判员(.*)", content_list[i])
                if temp9:
                    item['acting_judge'] += temp9[0] + " "
                temp10 = re.findall("(.*日$)", content_list[i])
                if temp10:
                    item['date'] += temp10[0] + " "
                temp11 = re.findall("^书\s*记\s*员(.*)", content_list[i])
                if temp11:
                    item['court_clerk'] += temp11[0] + " "
                temp12 = re.findall("法官助理(.*)", content_list[i])
                if temp12:
                    item['judge_assistant'] += temp12[0] + " "
                item["content"] += content_list[i] + "\n"

            print(item)

        elif self.is_element_visible(3, (By.ID, "validateCode")):
            pass
            # self.
        else:
            print(self.driver.current_url)
            self.driver.refresh()
            self.open_pages_and_parse_detail()


if __name__ == '__main__':
    w = wenshu("ds87fg687sdf6g8sdf87g6s89")
    w.run()
    w.driver.close()
