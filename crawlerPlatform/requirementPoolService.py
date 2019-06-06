#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rabbitMq.rabbitMq import RabbitMQ
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum as QueueEnum
from fetchDataBase import *
import json


# 来自企业名录模块的需求
def bussinessDirectoryProcess(rabbitMq, source, message):
    # TBD: 自己库里查询, 否则丢给爬虫
    # print(message)
    # print(type(message))
    search = json.loads(message)
    print(search)
    # print(type(search))
    print(source)

    # flag = is_chinese(message)
    # rs = get_ty_id(flag, message)
    rs = is_in_database(search)
    print(rs)
    if rs:
        print(message + " already in database !")
    else:
        print("bd Queue:" + str(search) + " source:" + str(source))
        # rabbitMq.sendMessage(RabbitMQ.QUEUE_PASS_ASREQ, "hello", 10)
        # 发布给爬虫模块
        priority = 10
        rabbitMq.publishMessage(QueueEnum.TOPIC_CRAWLER.getKey(), message, priority, source)


# 来自其他应用系统的需求，优先级较高
def appcationSystemProcess(rabbitMq, source, message):
    # TBD: 根据规则查询, 高优先级回复
    # print(RabbitMQ.getQueueName(method))
    print("as Queue:" + message + " source:" + str(source))
    priority = 10
    rabbitMq.publishMessage(QueueEnum.TOPIC_CRAWLER.getKey(), message, priority, source)


if __name__ == "__main__":
    # 初始化rabbitMq, 企业名录池
    rabbitMq = RabbitMQ()
    # rabbitMqBD.connect()
    threadBD = rabbitMq.recvMessage_async(QueueEnum.QUEUE_PASS_BDREQ.getKey(), bussinessDirectoryProcess)
    # threadAS = rabbitMq.recvMessage_async(QueueEnum.QUEUE_PASS_ASREQ.getKey(), appcationSystemProcess)
    threadBD.join()
    # threadAS.join()
    rabbitMq.close()
