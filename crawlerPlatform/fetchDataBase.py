import pymysql
import json
from crawlerDocuments.get_datebase import *


def get_serchKey():
    conn = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # sql = "select company,scode,data_acquisition_time from business_directory b WHERE (to_days(now()) - to_days(b.data_acquisition_time))>1 and b.data_acquisition_time is not null or b.data_acquisition_time is null order by rand() limit 1"
    sql = "select company,scode from business_directory b WHERE b.scode='91330206MA2GQENQ4Y'"
    cursor.execute(sql)
    rs = cursor.fetchall()
    return rs


def update_data_acquisition_time(flag, key, utime):
    conn = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
    cursor = conn.cursor()
    if flag:
        sql = "UPDATE business_directory b SET b.data_acquisition_time='" + utime + "' WHERE b.company='" + key + "'"
    else:
        sql = "UPDATE business_directory b SET b.data_acquisition_time='" + utime + "' WHERE b.scode='" + key + "'"
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return True


def get_ty_id(flag, key):
    conn = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset='utf8')
    cursor = conn.cursor()
    if flag:
        sql = "select * from tp_com where com_name='" + key + "'"
    else:
        sql = "select * from tp_com where creditCode='" + key + "'"
    cursor.execute(sql)
    rs = cursor.fetchall()
    conn.commit()
    conn.close()
    return rs


def is_in_database(message):
    message=databaseTool.unify_character_from_item(message)
    conn = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset='utf8')
    cursor = conn.cursor()
    # company=message['company'].
    cursor.execute(
        "select * from  base_info where Enterprise_name='" + message['company'] + "' order by id desc limit 1")
    com_name = cursor.fetchall()
    scode = None
    if message['scode']:
        cursor.execute(
            "select * from  base_info where Enterprise_tyshxydm='" + message['scode'] + "' order by id desc limit 1")
        scode = cursor.fetchall()

    flag = False
    if com_name or scode:
        flag = True
    return flag


def is_in_database2222(message):
    conn = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset='utf8')
    cursor = conn.cursor()
    cursor.execute(
        "select * from  gsxt where entName='" + message['company'] + "' order by id desc limit 1")
    com_name = cursor.fetchall()
    scode = None
    if message['scode']:
        cursor.execute(
            "select * from  gsxt where uniscId='" + message['scode'] + "' order by id desc limit 1")
        scode = cursor.fetchall()
    print(com_name)
    print(scode)
    flag = False
    if com_name or scode:
        print("541286")
        flag = True
    return flag


def insert_holder_info(main_id, item):
    item = databaseTool.unify_character_from_item(item)
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO `shareholder` (`c_id`,`shareholder`, `shareholder_type`, `blic_type`, `blic_number`, `ent_type`, `con_capital`, `con_capital_date`, `con_paid_in_capital`, `paid_in_capital_date`, `share_ratio`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (main_id,
                         item['shareholder'], item['shareholder_type'], item['blic_type'], item['blic_number'],
                         item['ent_type'],
                         item['con_capital'], item['con_capital_date'], item['con_paid_in_capital'],
                         item['paid_in_capital_date'],
                         item['share_ratio']))
    db.commit()
    cursor.close()
    db.close()


def get_tyc_holder(ty_id):
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from tp_holder t  where t.c_id='" + str(ty_id) + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result


def get_each_data(message):
    search_json = databaseTool.unify_character_from_item(json.loads(message))
    # search_json = message
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    print("getdata from database", search_json['company'])
    # flag = is_chinese(message)
    cursor.execute("select * from gsxt where entName='" + search_json['company'] + "' order by id desc limit 1")
    gsxt_base = cursor.fetchone()
    cursor.execute("select * from tp_com where com_name='" + search_json['company'] + "' order by id desc limit 1")
    tyc_base = cursor.fetchone()
    cursor.close()
    db.close()
    print("gsxt_base ", (gsxt_base))
    print("tyc_base ", (tyc_base))
    return gsxt_base, tyc_base


def get_gsxt_holder(gsxt_id):
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from gx_holder m  LEFT JOIN gx_holder_con mc ON m.id=mc.c_id LEFT JOIN gx_holder_rea mr ON m.id=mr.c_id where m.c_id='" + str(
        gsxt_id) + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result


def get_gx_branch(gsxt_id):
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from gx_branch where c_id=%s"
    cursor.execute(sql, str(gsxt_id))
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result


def get_tyc_branch(ty_id):
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from tp_branch where c_id=%s"
    cursor.execute(sql, ty_id)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result


def select_main_id(com_name):
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = "select id from base_info where Enterprise_name='" + com_name + "' order by id desc limit 1"
    cursor.execute(sql)
    idd = cursor.fetchone()
    cursor.close()
    db.close()
    if idd:
        return idd
    else:
        return None


def insert_branch_info(main_id, item):
    item = databaseTool.unify_character_from_item(item)
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = 'INSERT INTO `branch` (`c_id`, `branch_name`, `credit_code`, `Enterprise_gszch`, `reg_authority`, `legal_person`, `industry`, `estiblish_date`, `business_state`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    cursor.execute(sql, (
        main_id, item['branch_name'], item['credit_code'], item['Enterprise_gszch'], item['reg_authority'],
        item['legal_person'], item['industry'], item['estiblish_date'], item['business_state']))
    db.commit()
    cursor.close()
    db.close()


def insert_base_info(item):
    item = databaseTool.unify_character_from_item(item)
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO `base_info` (`Enterprise_name`, `Enterprise_tyshxydm`, `Legalrepresentative`, `Enterprise_zzjgdm`, `Enterprise_gszch`, `rtime`, `registered_address`, `gslx`, `jyzt`, `op_from`, `op_to`, `approval_date`, `djjg`, `f_body`, `reasons_cancel`, `zczb`, `paid_in_capital`, `ygrs`, `social_staff_num`, `industry`, `Contact_number`, `email`, `z_body`, `source_update_time`, `local_update_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (
        item['Enterprise_name'], item['Enterprise_tyshxydm'], item['Legalrepresentative'], item['Enterprise_zzjgdm'],
        item['Enterprise_gszch'], item['rtime'], item['registered_address'], item['gslx'], item['jyzt'],
        item['op_from'],
        item['op_to'], item['approval_date'], item['djjg'], item['f_body'], item['reasons_cancel'], item['zczb'],
        item['paid_in_capital'], item['ygrs'], item['social_staff_num'], item['industry'], item['Contact_number'],
        item['email'], item['z_body'], item['source_update_time'], item['local_update_time']))
    db.commit()
    cursor.close()
    db.close()


def is_chinese(string):
    for chart in string:
        if '\u4e00' <= chart <= '\u9fa5':
            return True
    return False


if __name__ == '__main__':
    # key={}
    key = {"company": "中国农发重点建设基金有限公司", "scode": "91110000717846134F"}
    is_in_database2222(key)
