#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import threading

from rabbitMq.rabbitMq import RabbitMQ
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum as QueueEnum
from fetchDataBase import *
import datetime
from dataggregateDemo2 import *
import json

data_id_list = {}


def aggregationProcess(rabbitMq, source, message):
    print(source)
    print(message)
    get_each_data_message = message
    search_json = json.loads(message)
    print(search_json)
    if search_json['scode']:
        message = search_json['scode']
    else:
        message = search_json['company']
    if message not in data_id_list:
        print("add message to data_id_list")
        data_id_list.update({message: 0})
    offset = int(source) - 51
    bitmap = data_id_list[message]
    temp = 1 << offset
    data_id_list.update({message: bitmap | temp})
    print(data_id_list)
    if bin(data_id_list[message]) == '0b1111':
        data_id_list.pop(message)
        # 获取基础数据
        gsxt_base, tyc_base = get_each_data(get_each_data_message)
        # 进行数据整合
        deal_each_data(gsxt_base, tyc_base)
        # print("send to aggregation database")


if __name__ == "__main__":
    rabbitMq = RabbitMQ()
    threadResp = rabbitMq.recvMessage_async(QueueEnum.QUEUE_PASS_DAGREQ.getKey(), aggregationProcess)
    threadResp.join()
    rabbitMq.close()
