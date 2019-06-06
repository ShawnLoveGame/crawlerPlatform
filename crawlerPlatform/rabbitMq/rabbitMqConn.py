import pika
import configparser
import time
import traceback
from rabbitMq.rabbitMqQueue import RabbitMQQueueEnum as QueueEnum


class RabbitMQConn:
    def __init__(self, queue, topic, callback):
        self.retryIntval = 3  # 3秒后重试
        self.connetion = None
        self.readConfig()
        self.connect()
        self.connectName = queue
        self.queueCallback = callback
        if queue is not None:
            self.declareQueue(queue, callback)
        self.sendQueueList = []
        self.topic = topic
        if topic is not None:
            self.declareTopic(topic)

    def readConfig(self):
        # 读取配置文件
        cf = configparser.ConfigParser()
        # TBD: 目录调整
        cf.read("rabbitMq/config.conf")
        # 读取配置信息
        self.host = cf.get("rabbitMq", "host")
        self.credentials = pika.PlainCredentials(cf.get("rabbitMq", "username"), cf.get("rabbitMq", "password"))
        # print(self.credentials)
        self.port = cf.get("rabbitMq", "port")
        self.vhost = cf.get("rabbitMq", "vhost")
        # print(self.host)

    def connect(self):
        # 连接rabbitMq服务器
        try:
            parameter = pika.ConnectionParameters(self.host, self.port, self.vhost, self.credentials,heartbeat=0)
            # print("!!!!!!!!!!!!!!!!!!!!")
            self.connection = pika.BlockingConnection(parameter)

            # print("**********************")
        except:
            # 连接失败, 重新读取文件
            self.readConfig()
            print("connect error, try to reconnect Server:" + self.host + ":" + self.port)
            time.sleep(self.retryIntval)
            self.connect()
        else:
            self.channel = self.connection.channel()

    def declareQueue(self, queue, callback):
        try:
            self.queue = self.channel.queue_declare(queue=queue, durable=True)
        except:
            print("declare queue error.")

        if callback is not None:
            self.queueCallback = callback

    def recvMessage(self):
        self.channel.basic_consume(queue=self.connectName, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, channel, method, properties, message):
        # print("[" + str(method.routing_key) + "]recv message:" + message.decode('utf-8'))
        # 根据queue(routing_key)来查找回调
        messageData = message.decode('utf-8')
        messageSource = messageData[0:2]
        messageBody = messageData[2:]
        if self.queueCallback is not None:
            self.queueCallback(self, int(messageSource), messageBody)

    def sendMessage(self, queue, message, priority, source=0):
        message = ('%02d' % (source)) + message
        # 简单处理, 保证队列创建, 无需对应创建channel
        if queue not in self.sendQueueList:
            try:
                self.declareQueue(queue, None)
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('e.message:\t', e.args)
                print('traceback.print_exc():', traceback.print_exc())
                print('traceback.format_exc():\n%s' % traceback.format_exc())
            self.sendQueueList.append(queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                       priority=priority,
                                       content_encoding="utf-8"))

    def declareTopic(self, topic):
        self.channel.exchange_declare(exchange=topic, exchange_type='fanout')
        if self.connectName is not None:
            self.queue = self.channel.queue_declare(queue=self.connectName, durable=True)
            self.channel.queue_bind(exchange=topic, queue=self.connectName, routing_key=self.connectName)

    def publishMessage(self, topic, message, priority, source=0):
        message = ('%02d' % (source)) + message
        # 默认发送消息, 发布消息topic
        self.channel.basic_publish(
            exchange=topic,
            routing_key='',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                priority=priority,
                content_encoding="utf-8"
            ))

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def getMessageCount(self, queue):
        return self.channel.queue_declare(queue=queue, durable=True).method.message_count
