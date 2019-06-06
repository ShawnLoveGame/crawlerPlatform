import requests
from urllib.parse import quote
import json
import pymysql
from requests.exceptions import RequestException
import sys
from retrying import retry
from pybloom_live import ScalableBloomFilter
from  crawlerDocuments.SetProxy import Ss
import time

class Fy():
    def __init__(self,keyword):
        self.host = '192.168.1.68'
        self.user = 'root'
        self.pwd = '123456'
        self.database = 'mytest'
        self.keyword=keyword
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,es;q=0.9,es-ES;q=0.8,zh-CN;q=0.7',
            'content-length': '1046',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            #'cookie': 'UM_distinctid=1696ac78dccfb-009f7a2d6ee17d-9393265-100200-1696ac78dcf1fb; CNZZDATA1273632440=347324338-1552274654-https%253A%252F%252Fwww.baidu.com%252F%7C1552629568; LFR_SESSION_STATE_20158=1552635997234; tgw_l7_route=d6024730f715155a79371f0da3690819; JSESSIONID=7D9076B4F998D208F5195B570D04F33C',
            'dnt': '1',
            'origin': 'https://rmfygg.court.gov.cn',
            # 'referer': 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?content=%E7%A6%8F%E5%BB%BA%E8%AF%9A%E5%8D%8E',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.proxy={}
        self.ss= Ss()
        self.data = {

        }

    @retry(stop_max_attempt_number=100)
    def get_PROXY(self):
        # 获取代理
        json_p = self.ss.getOne('fygg')
        host = str(json_p['ip'])
        port = str(json_p['port'])
        hostport = host + ':' + port
        self.proxy.update({'http': hostport})
        json_ps = self.ss.getOnes('fygg')
        hosts = str(json_ps['ip'])
        ports = str(json_ps['port'])
        hostports = hosts + ':' + ports
        self.proxy.update({'https': hostports})
        print("ip端口响应正常")
        print(self.proxy)
        try:
            resopnse=requests.get('https://rmfygg.court.gov.cn/', headers=self.headers, proxies=self.proxy,timeout=7)
            print(resopnse.status_code)
        except:
            self.ss.setFalse(str(json_p['ip']),str(json_p['port']), 'fygg')
            self.ss.setFalse(str(json_ps['ip']),str(json_ps['port']), 'fygg')
            raise Exception
        print("该IP可访问网站")
        print(self.proxy)
    def run(self):
        #self.get_PROXY()
        search_list = self.get_search_list()
        index_index = 1
        # for se in search_list:
        #     key = se['com_name']
        #     print(" 搜索关键字")
        #     print(key)
        #     if index_index % 15 == 0:  # 五条数据换ip
        #         pass
                #self.get_PROXY()
            # key = sys.argv[1]
        url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?content={}'.format(quote(self.keyword))
        self.headers.update({'referer': url})
        self.data.update({'_noticelist_WAR_rmfynoticeListportlet_searchContent': self.keyword})
        dataS = '[{"name":"sEcho","value":1},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
        self.data.update({'_noticelist_WAR_rmfynoticeListportlet_aoData': dataS})
        post_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1'
        start_time=time.time()
        html = self.get_index(post_url)
        #if html is not 'no_json':
        json_data = json.loads(html)
        TotalRecords = int(json_data['iTotalRecords'])
        print("总条数")
        print(TotalRecords)
        dataS_format = '[{"name":"sEcho","value":{}},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":{}},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
        index = 1
        start = 0
        data_sql="select gtype,tosendPeople,court,publishDate,noticeCode,noticeContent from court_noun"
        b=self.get_bloomFilter(data_sql)
        while TotalRecords > 0:
            dataS = '[{"name":"sEcho","value":' + str(
                index) + '},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":' + str(
                start) + '},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
            self.data.update({'_noticelist_WAR_rmfynoticeListportlet_aoData': dataS})
            print(dataS)
            html = self.get_index(post_url)
            #if html is not 'no_json':
            TotalRecords -= 15
            index += 1
            start += 15
            print(html)
            json_data = json.loads(html)
            data = json_data['data']
            for i in range(len(data)):
                item = {}
                # 公告类型
                item['gtype'] = data[i]['noticeType']
                # 被告人
                item['tosendPeople'] = data[i]['tosendPeople']
                # 法院
                item['court'] = data[i]['court']
                # 刊登日期
                item['publishDate'] = data[i]['publishDate']
                # 公告号
                item['noticeCode'] = data[i]['noticeCode']
                # 公告内容
                item['noticeContent'] = data[i]['noticeContent']
                # item['publishDate'] = data[i]['publishDate']
                print("get")
                if item in b:
                    print("已在数据库")
                else:
                    b.add(item)
                    self.insert_fygg_info(item)
            end_time=time.time()
            print("搜索速度")
            print(end_time - start_time)
            if (end_time - start_time) < 30:
                if 30 - (end_time - start_time)<10:
                    time.sleep(10)
                else:
                    time.sleep(30 - (end_time - start_time))
            print("搜索条数")
            print(index_index)
            index_index+=1
            # print(html)
    def get_bloomFilter(self, sql):
        bloom = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        db = pymysql.connect("localhost", "root", "123456", "mytest", charset='utf8')
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
    def insert_fygg_info(self,item):
        db = pymysql.connect(self.host, self.user, self.pwd, self.database, charset='utf8')
        sql = "insert into court_noun(gtype,tosendPeople,court,publishDate,noticeCode,noticeContent) values (%s,%s,%s,%s,%s,%s)"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (
                item['gtype'], item['tosendPeople'], item['court'], item['publishDate'], item['noticeCode'],
                item['noticeContent']))
            db.commit()
            db.close()
        except RequestException as err:
            print(err)
            print(sql)
    @retry(stop_max_attempt_number=10)
    def get_index(self, url):
        response = requests.post(url, headers=self.headers, data=self.data,proxies=self.proxy)
        try:
            print(response.text)
            json.loads(response.text)
            return response.text
        except:
            print("睡眠一分钟")
            time.sleep(60)
            raise Exception
            #return  "no_json"
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

if __name__ == '__main__':
    f = Fy("sdfas")
    f.run()
