import pymysql
import json
from fetchDataBase import *
import threading
import operator
import time
import datetime
from pybloom_live import BloomFilter, ScalableBloomFilter


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


class databaseTool:
    @staticmethod
    def collection_field(*args):
        field = None
        temp = None
        for arg in args:
            # print("TYPE OF ARG :",type(arg))
            print("ARG :", (arg))
            if arg:
                # print("11111111111111111111111")
                if isinstance(arg, datetime.datetime):
                    # print("2222222222222222222222")
                    if not temp:
                        # print("333333333333333333333")
                        temp = arg
                    else:
                        # print("44444444444444444444")
                        print("temp", temp)
                        print("arg ", arg)
                        print("arg-temp :", temp - arg)
                        print((temp - arg).total_seconds())
                        if (temp - arg).total_seconds() < 0:
                            temp = arg
                    field = temp
                else:
                    field = arg
                    break
        return field

    @staticmethod
    def select_main_field(*args):
        main_field = None
        for arg in args:
            if arg:
                main_field = arg
                break
        print("main_field : ", main_field)
        return main_field

    @staticmethod
    def field_append(*args):
        list = databaseTool.removeDuplicate(*args)
        field = ""
        if list[0][0]:
            field += str(list[0][0]) + "(" + databaseTool.get_tag(list[0][1]) + ")"
        flag = True
        for i in range(1, len(list)):
            if list[i][0]:
                if list[i][0] != "None":
                    flag = False
                    field += str(list[i][0]) + "(" + databaseTool.get_tag(list[i][1]) + ")"
        if flag:
            if "None" in field:
                field = ''
        return field

    @staticmethod
    def get_tag(num):
        tag = ""
        if num == 0:
            tag = "GX"
        if num == 1:
            tag = "TYC"
        return tag

    @staticmethod
    def collection_list_field(list, data, main_field):
        if list:
            bloom = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
            for l in list:
                bloom.add(l)
            if data not in bloom:
                for l in list:
                    if l[main_field] == data[main_field]:
                        list.remove(l)
                        item = {}
                        for k, v in l.items():
                            item[k] = databaseTool.collection_field(databaseTool.is_field_dict(l, k),
                                                                    databaseTool.is_field_dict(data, k))
                        list.append(item)
                    else:
                        list.append(data)
        else:
            list.append(data)
        return list

    @staticmethod
    def removeDuplicate(*args):
        field_item = {}
        for i in range(len(args) - 1, -1, -1):
            field_item.update({args[i]: i})
        sortedDist = sorted(field_item.items(), key=operator.itemgetter(1), reverse=False)
        return sortedDist

    @staticmethod
    def is_field_dict(d, f):
        if d:
            if f in d:
                print("d[f] : ", d[f])
                return databaseTool.clear_field(d[f])
            else:
                return None
        else:
            return None

    @staticmethod
    def clear_field(obj):
        print(type(obj))
        clear_obj = obj
        if obj == "None":
            clear_obj = ""
        if obj == "-":
            clear_obj.replace("-", "")
        if isinstance(clear_obj, str):
            clear_obj.replace("\n", "")
            if clear_obj.isdigit():
                if len(clear_obj) == 13:
                    timeStamp = float(int(clear_obj) / 1000)
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    clear_obj = str(otherStyleTime)

        return clear_obj

    @staticmethod
    def unify_character(o):
        if isinstance(o, str):
            o = o.replace("（", "(").replace("）", ")").replace("<", "(").replace(">", ")")
            if o.startswith("` "):
                o.replace("` ", "")
        return o

    @staticmethod
    def unify_character_from_item(item):
        new_item = {}
        for k, v in item.items():
            new_item[k] = databaseTool.unify_character(item[k])
        return new_item

    # 重复字典分组
    @staticmethod
    def dup_divide(item_list):
        a = []
        x = []
        for i in range(0, len(item_list)):
            if i + 1 < len(item_list):
                if item_list[i]['shareholder'] == item_list[i + 1]['shareholder']:
                    x.append(item_list[i])
                else:
                    x.append(item_list[i])
                    a.append(x)
                    x = []
            else:
                x.append(item_list[len(item_list) - 1])
                a.append(x)
        print(a)
        return a


if __name__ == '__main__':
    # databaseTool.removeDuplicate(None, None, "C", "D")
    # dt1 = datetime.datetime.strptime('2017-04-19 00:42:44', '%Y-%m-%d %H:%M:%S')
    # dt2 = datetime.datetime.strptime('2017-05-19 00:42:44', '%Y-%m-%d %H:%M:%S')
    # dt = databaseTool.collection_field(None, dt1, None, dt2, None)
    # print(dt)

    item = {"1": "<a>", "2": "（b）", "3": "asfd", "4": 8}
    new = databaseTool.unify_character_from_item(item)
    print(new)
