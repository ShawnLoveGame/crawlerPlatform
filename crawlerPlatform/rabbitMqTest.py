#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rabbitMq.rabbitMq import RabbitMQ
import time
import pika
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum

#初始化rabbitMq
#rabbitMq = RabbitMQ()
#rabbitMq.sendMessage(RabbitMQQueueEnum.QUEUE_PASS_BDREQ.getKey(), "福建诚华aaasdfsadf123-1", 1, RabbitMQQueueEnum.QUEUE_PASS_BDREQ.getValue())
#rabbitMq.sendMessage(RabbitMQQueueEnum.QUEUE_PASS_ASREQ.getKey(), "福州测试1231231adasfdasdf-1", 10)

#rabbitMq.sendMessage(RabbitMQ.QUEUE_PASS_BDREQ, "福建诚华aaasdfsadf123-2", 1)
#rabbitMq.sendMessage(RabbitMQ.QUEUE_PASS_ASREQ, "福州测试1231231adasfdasdf-2", 10)

#print (rabbitMq.getQueueMessageCount(rabbitMq.QUEUE_BD_REQ))

#rabbitMq.test()

rabbitMq = RabbitMQ()
rabbitMq.publishMessage(RabbitMQQueueEnum.TOPIC_CRAWLER.getKey(), "test1111", 19)
rabbitMq.publishMessage(RabbitMQQueueEnum.TOPIC_CRAWLER.getKey(), "test1111", 19)
#rabbitMq.publishMessage(RabbitMQ.TOPIC_CRAWLER, "test1111", 19)
#rabbitMq.publishMessage(RabbitMQ.TOPIC_CRAWLER, "test1111", 19)

rabbitMq.close()

#enum = RabbitMQQueueEnum()
#print(RabbitMQQueueEnum.getQueueName(RabbitMQQueueEnum.QUEUE_PASS_BDREQ))
#print(RabbitMQQueueEnum.getQueueValue(RabbitMQQueueEnum.QUEUE_PASS_BDREQ))
#print(RabbitMQQueueEnum.getQueueNameByValue(1))


#strTest = print("%02d", 0)
#print(strTest)