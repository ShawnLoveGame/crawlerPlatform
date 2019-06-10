#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import threading
from rabbitMq.rabbitMq import RabbitMQ
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum as QueueEnum
from crawlerDocuments.TyPhone import Tphone
from crawlerDocuments.zhixing import Zhi
from crawlerDocuments.fygg import Fy
from crawlerDocuments.wenshuWithSelenium import wenshu
from crawlerDocuments.gsxt import GSXT
import json


def tycCallback(rabbitMq, source, message):
    searchKey = json.loads(message)
    # 网站爬取
    print("tycCallback source: ", source)
    print("tyc recv:" + str(searchKey) + " from:" +
          QueueEnum.getQueueNameBySource(source))
    if searchKey['scode']:
        key = searchKey['scode']
    else:
        key = searchKey['company']
    ty = Tphone(key)
    ty.run()
    # 告诉企业需求分析池
    priority = 10
    print()
    if source == QueueEnum.QUEUE_PASS_BDREQ.getValue():
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_BDRESP.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_TYC.getValue())
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_TYC.getValue())


def gjgsCallback(rabbitMq, source, message):
    searchKey = json.loads(message)
    print("gjgsCallback source: ", source)
    print("gjgs recv:" + str(searchKey))
    if searchKey['scode']:
        key = searchKey['scode']
    else:
        key = searchKey['company']
    g = GSXT(key)
    g.main()
    messageDone = message + " done."
    priority = 10
    if source == QueueEnum.QUEUE_PASS_BDREQ.getValue():
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_BDRESP.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_GJGS.getValue())
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_GJGS.getValue())


def zhixingCallback(rabbitMq, source, message):
    searchKey = json.loads(message)
    print("zhixingCallback source: ", source)
    print("zhixing recv:" + str(searchKey))
    if searchKey['scode']:
        key = searchKey['scode']
    else:
        key = searchKey['company']
    # z = Zhi(key)
    # z.run()
    priority = 10
    if source == QueueEnum.QUEUE_PASS_BDREQ.getValue():
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_BDRESP.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_ZHIXING.getValue())
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_ZHIXING.getValue())


def fyggCallback(rabbitMq, source, message):
    searchKey = json.loads(message)
    print("wenshuCallback source: ", source)
    print("wenshu recv:" + str(searchKey))
    messageDone = message + " done."
    if searchKey['scode']:
        key = searchKey['scode']
    else:
        key = searchKey['company']
    f = Fy(key)
    f.run()
    priority = 10
    if source == QueueEnum.QUEUE_PASS_BDREQ.getValue():
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_BDRESP.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_FYGG.getValue())
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_FYGG.getValue())


def wenshuCallback(rabbitMq, source, message):
    searchKey = json.loads(message)
    print("wenshuCallback source: ", source)
    print("wenshu recv:" + str(searchKey))
    messageDone = message + " done."
    if searchKey['scode']:
        key = searchKey['scode']
    else:
        key = searchKey['company']
    # w = wenshu(key)
    # w.run()
    priority = 10
    if source == QueueEnum.QUEUE_PASS_BDREQ.getValue():
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_BDRESP.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_WENSHU.getValue())
        rabbitMq.sendMessage(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), message, priority,
                             QueueEnum.QUEUE_CRAWLER_WENSHU.getValue())


if __name__ == "__main__":
    # 初始化rabbitMq, 企业名录池
    rabbitMq = RabbitMQ()
    threadGjgs = rabbitMq.subscribeMessage_async(QueueEnum.TOPIC_CRAWLER.getKey(),
                                                 QueueEnum.QUEUE_CRAWLER_GJGS.getKey(), gjgsCallback)
    threadTycList = []
    for i in range(1):
        threadTyc = rabbitMq.subscribeMessage_async(QueueEnum.TOPIC_CRAWLER.getKey(),
                                                    QueueEnum.QUEUE_CRAWLER_TYC.getKey(),
                                                    tycCallback)
        threadTycList.append(threadTyc)

    threadZhixing = rabbitMq.subscribeMessage_async(QueueEnum.TOPIC_CRAWLER.getKey(),
                                                    QueueEnum.QUEUE_CRAWLER_ZHIXING.getKey(),zhixingCallback)
    # threadFygg = rabbitMq.subscribeMessage_async(QueueEnum.TOPIC_CRAWLER.getKey(),
    #                                              QueueEnum.QUEUE_CRAWLER_FYGG.getKey(), fyggCallback)
    threadWenshu = rabbitMq.subscribeMessage_async(QueueEnum.TOPIC_CRAWLER.getKey(),
                                                   QueueEnum.QUEUE_CRAWLER_WENSHU.getKey(), wenshuCallback)
    threadGjgs.join()
    threadZhixing.join()
    # threadFygg.join()
    threadWenshu.join()
    for threadTyc in threadTycList:
        threadTyc.join()

    rabbitMq.close()
