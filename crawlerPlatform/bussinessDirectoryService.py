#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import threading

from rabbitMq.rabbitMq import RabbitMQ
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum as QueueEnum
from fetchDataBase import *
import datetime
import json

# 爬虫模块反馈查询完成, 更新数据库
def respDataProcess(rabbitMq, source, message):
    # 更新自己日期到自己的数据库
    print(source)
    print(type(source))

    # print("respDataProcess message:" + message+ "  Done !!!")
    # uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # flag = is_chinese(message)
    # update_data_acquisition_time(flag, message, uptime)

    # rabbitMqSend.sendMessage(rabbitMqSend.QUEUE_AS_REQ, "测试发送", 10)


# 读取数据库, 进行查询
def fetchDataProcess():
    rabbitMq = RabbitMQ()
    messageLimit = 1000
    ket_list = get_serchKey()
    index = 0
    while True:
        messageCount = rabbitMq.getMessageCount(QueueEnum.QUEUE_PASS_BDREQ.getKey())
        fetchCount = messageLimit - messageCount
        if fetchCount > 0:
            print("fetch data from database. messageCount = " + str(messageCount))
            for key in ket_list[index:index + 10]:
                # if key['scode']:
                #     message = key['scode']
                # else:
                #     message = key['company']
                message = json.dumps(key)
                priority = 10
                source = QueueEnum.QUEUE_PASS_BDREQ.getValue()
                queue = QueueEnum.QUEUE_PASS_BDREQ.getKey()
                # if num % 2 == 0:
                #     queue = QueueEnum.QUEUE_PASS_ASREQ.getKey()
                #     source = QueueEnum.QUEUE_PASS_ASREQ.getValue()
                print("send data to Queue:" + queue)
                rabbitMq.sendMessage(queue, message, priority, source)
            index += 10
        if index > len(ket_list):
            break
        time.sleep(60)
    rabbitMq.close()


if __name__ == "__main__":
    rabbitMq = RabbitMQ()
    threadResp = rabbitMq.recvMessage_async(QueueEnum.QUEUE_PASS_BDRESP.getKey(), respDataProcess)
    threadFetch = threading.Thread(target=fetchDataProcess)
    threadFetch.start()
    threadFetch.join()
    threadResp.join()

    rabbitMq.close()
