#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pika
import threading

from rabbitMq.rabbitMqConn import RabbitMQConn

class RabbitMQ():
    def __init__(self):
        self.defaultRabitMQ = None
        self.queueConnList = []
        self.topicConnList = []

    #TBD: 优先级不生效问题
    def sendMessage(self, queue, message, priority, source = 0):
        #发送不需要单独channel, 可以直接复用
        if self.defaultRabitMQ is None:
            self.defaultRabitMQ = RabbitMQConn(queue, None, None)
        rabbitMq = self.defaultRabitMQ
        rabbitMq.sendMessage(queue, message, priority, source)

    #同步执行, 无消息时会阻塞住
    def recvMessage(self, queue, callback):
        rabbitMqConn = RabbitMQConn(queue, None, callback)
        self.queueConnList.append(rabbitMqConn)
        rabbitMqConn.queueCallback = callback
        rabbitMqConn.recvMessage()

    def recvMessage_async(self, queue, callback):
        thread = threading.Thread(target = self.recvMessage, args = (queue, callback,))
        thread.start()
        return thread

    #TBD: 发布的时候, 无消息队列, 自动创建
    def publishMessage(self, topic, message, priority, source = 0):
        if self.defaultRabitMQ is None:
            self.defaultRabitMQ = RabbitMQConn(None, topic, None)
        rabbitMq = self.defaultRabitMQ
        rabbitMq.publishMessage(topic, message, priority, source)

    # 同步执行, 无消息时会阻塞住
    def subscribeMessage(self, topic, queue, callback):
        #每次新建一条连接
        rabbitMqConn = RabbitMQConn(queue, topic, callback)
        self.topicConnList.append(rabbitMqConn)
        rabbitMqConn.queueCallback = callback
        rabbitMqConn.recvMessage()

    def subscribeMessage_async(self, topic, queue, callback):
        thread = threading.Thread(target = self.subscribeMessage, args = (topic, queue, callback,))
        thread.start()
        return thread

    #TBD: 获取消息队列数量
    def getMessageCount(self, queue):
        if self.defaultRabitMQ is not None:
            rabbitMq = self.defaultRabitMQ
        else:
            self.defaultRabitMQ = RabbitMQConn(queue, None, None)
            rabbitMq = self.defaultRabitMQ

        return rabbitMq.getMessageCount(queue)

    def close(self):
        for conn in self.queueConnList:
            conn.close()
        for conn in self.topicConnList:
            conn.close()
