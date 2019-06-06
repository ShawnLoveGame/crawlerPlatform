class Queue:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

class RabbitMQQueueEnum:
    # 队列定义, 需要区分来自企业名录的需求和来自应用系统的需求
    # 队列名需求, 按以下格式: 转发模式.交换机名.队列名
    # 转发格式: 单播: direct 广播: fanout 主题:topic
    # 交换机名: 默认为passEx,表示只做传递, 只有需要单独队列时, 需要重新设置
    # 例子:  direct.passEx.dataQ
    QUEUE_PASS_DEFAULT = Queue("direct.passEx.default", 0)
    QUEUE_PASS_BDREQ = Queue("direct.passEx.BDReq", 1)
    QUEUE_PASS_BDRESP = Queue("direct.passEx.BDResp", 2)
    QUEUE_PASS_ASREQ = Queue("direct.passEx.ASReq", 3)
    QUEUE_PASS_DAGREQ = Queue("direct.passEx.ASReq", 4)

    TOPIC_CRAWLER = Queue("crawlerEx", 30)

    QUEUE_CRAWLER_GJGS = Queue("fanout.crawlerEx.gjgs", 51)
    QUEUE_CRAWLER_TYC = Queue("fanout.crawlerEx.tyc", 52)
    QUEUE_CRAWLER_ZHIXING = Queue("fanout.crawlerEx.zhixing", 53)
    QUEUE_CRAWLER_WENSHU = Queue("fanout.crawlerEx.wenshu", 54)

    QUEUE_CRAWLER_FYGG = Queue("fanout.crawlerEx.fygg", 55)

    # 加入list保存
    queueList = []
    queueList.append(QUEUE_PASS_DEFAULT)
    queueList.append(QUEUE_PASS_BDREQ)
    queueList.append(QUEUE_PASS_BDRESP)
    queueList.append(QUEUE_PASS_ASREQ)
    queueList.append(TOPIC_CRAWLER)
    queueList.append(QUEUE_CRAWLER_GJGS)
    queueList.append(QUEUE_CRAWLER_TYC)

    @staticmethod
    def getQueueName(queue):
        return queue.getKey()

    @staticmethod
    def getQueueValue(queue):
        return queue.getValue()

    @staticmethod
    def getQueueNameBySource(value):
        for queue in RabbitMQQueueEnum.queueList:
            if queue.getValue() == value:
                return queue.getKey()
        return "default"

