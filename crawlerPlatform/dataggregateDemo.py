from crawlerDocuments.get_datebase import *
import pymysql
import json
import threading


def get_each_data(message):
    search_json = json.loads(message)
    db = pymysql.connect("192.168.1.68", "root", "123456", "phtest", charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
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


def deal_each_data(gsxt_base, tyc_base):
    item = {}

    item['Enterprise_name'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'entName'),
                                                        databaseTool.is_field_dict(tyc_base, 'com_name'))

    item['Enterprise_tyshxydm'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'uniscId'),
                                                            databaseTool.is_field_dict(tyc_base, 'creditCode'))

    item['Legalrepresentative'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'person_name'),
                                                            databaseTool.is_field_dict(tyc_base,
                                                                                       'legalPersonName'))

    item['Enterprise_zzjgdm'] = databaseTool.field_append(None,
                                                          databaseTool.is_field_dict(tyc_base, 'orgNumber'))

    item['Enterprise_gszch'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'register_num'),
                                                         databaseTool.is_field_dict(tyc_base, 'regNumber'))

    item['rtime'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'estDate'),
                                              databaseTool.is_field_dict(tyc_base, 'estiblishTime'))

    item['registered_address'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'dom'),
                                                           databaseTool.is_field_dict(tyc_base, 'regLocation'))

    item['gslx'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'entType'),
                                             databaseTool.is_field_dict(tyc_base, 'companyOrgType'))

    item['jyzt'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'regState'),
                                             databaseTool.is_field_dict(tyc_base, 'regStatus'))

    item['op_from'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'opFrom'),
                                                databaseTool.is_field_dict(tyc_base, 'fromTime'))

    item['op_to'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'opTo'), None)

    item['approval_date'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'apprDate'),
                                                      databaseTool.is_field_dict(tyc_base, 'approvedTime'))

    item['djjg'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'regOrg'),
                                             databaseTool.is_field_dict(tyc_base, 'regInstitute'))

    item['f_body'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'opScope'),
                                               databaseTool.is_field_dict(tyc_base, 'businessScope'))

    item['reasons_cancel'] = databaseTool.field_append(databaseTool.is_field_dict(gsxt_base, 'cancel_reason'),
                                                       None)

    item['zczb'] = databaseTool.field_append(None,
                                             databaseTool.is_field_dict(tyc_base, 'regCapital'))

    item['paid_in_capital'] = databaseTool.field_append(None,
                                                        databaseTool.is_field_dict(tyc_base, 'actualCapital'))

    item['ygrs'] = databaseTool.field_append(None,
                                             databaseTool.is_field_dict(tyc_base, 'staffNumRange'))

    item['social_staff_num'] = databaseTool.field_append(None,
                                                         databaseTool.is_field_dict(tyc_base, 'socialStaffNum'))

    item['industry'] = databaseTool.field_append(None,
                                                 databaseTool.is_field_dict(tyc_base, 'industry'))

    item['Contact_number'] = databaseTool.field_append(None,
                                                       databaseTool.is_field_dict(tyc_base, 'phoneNumber'))

    item['email'] = databaseTool.field_append(None, databaseTool.is_field_dict(tyc_base, 'email'))

    item['z_body'] = databaseTool.field_append(None,
                                               databaseTool.is_field_dict(tyc_base, 'baseInfo'))
    item['source_update_time'] = databaseTool.field_append(None,
                                               databaseTool.is_field_dict(tyc_base, 'ty_update_time'))

    print(item)
    if item['Enterprise_name']:
        insert_base_info(item)
        main_id = select_main_id(item['Enterprise_name'])
        # 整合股东信息
        aggregate_holder_info(main_id, gsxt_base["id"], tyc_base["id"])


def aggregate_holder_info(main_id, gsxt_id, ty_id):
    item_list = set()
    thread_list = []
    gx_thread = MyThread(get_gsxt_holder, args=(gsxt_id,))
    thread_list.append(gx_thread)
    gx_thread.start()
    tyc_thread = MyThread(get_tyc_holder, args=(ty_id,))
    thread_list.append(tyc_thread)
    tyc_thread.start()
    for t in thread_list:
        t.join()
    tyc_holder_list = tyc_thread.get_result()
    gx_holder_list = gx_thread.get_result()

    # gx_holder_list = get_gsxt_holder(gsxt_id)
    if gx_holder_list:
        for holder in gx_holder_list:
            item = {}
            item['shareholder'] = holder["inv_name"]
            item['shareholder_type'] = holder["invType"]
            item['blic_type'] = holder["blicType"]
            item['blic_number'] = holder["bLicNo"]
            item['ent_type'] = holder["respForm"]
            item['con_capital '] = holder["subConAm"]
            item['con_capital_date'] = holder["conDate"]
            item['con_paid_in_capital'] = holder["acConAm"]
            item['paid_in_capital_date'] = holder["conDate"]
            item['share_ratio'] = None
            print("gx_holder_item : ", item)
            item_list.add(json.dumps(item))
    if tyc_holder_list:
        for holder in tyc_holder_list:
            item = {}
            item['shareholder'] = holder["person_name"]
            item['shareholder_type'] = None
            item['blic_type'] = None
            item['blic_number'] = None
            item['ent_type'] = None
            item['con_capital '] = holder["amomon"]
            item['con_capital_date'] = holder["h_time"]
            item['con_paid_in_capital'] = None
            item['paid_in_capital_date'] = None
            item['share_ratio'] = holder["percent"]
            print("tyc_holder_item : ", item)
            item_list.add(json.dumps(item))
    # for item in item_list:
    # print(item)
    # insert_holder_info(json.loads(item))


def insert_holder_info(item):
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO `shareholder` (`shareholder`, `shareholder_type`, `blic_type`, `blic_number`, `ent_type`, `con_capital`, `con_capital_date`, `con_paid_in_capital`, `paid_in_capital_date`, `share_ratio`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (
        item['shareholder'], item['shareholder_type'], item['blic_type'], item['blic_number'], item['ent_type'],
        item['con_capital'], item['con_capital_date'], item['con_paid_in_capital'], item['paid_in_capital_date'],
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


def insert_base_info(item):
    db = pymysql.connect("192.168.1.68", "root", "123456", "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO `base_info` (`Enterprise_name`, `Enterprise_tyshxydm`, `Legalrepresentative`, `Enterprise_zzjgdm`, `Enterprise_gszch`, `rtime`, `registered_address`, `gslx`, `jyzt`, `op_from`, `op_to`, `approval_date`, `djjg`, `f_body`, `reasons_cancel`, `zczb`, `paid_in_capital`, `ygrs`, `social_staff_num`, `industry`, `Contact_number`, `email`, `z_body`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (
        item['Enterprise_name'], item['Enterprise_tyshxydm'], item['Legalrepresentative'], item['Enterprise_zzjgdm'],
        item['Enterprise_gszch'], item['rtime'], item['registered_address'], item['gslx'], item['jyzt'],
        item['op_from'],
        item['op_to'], item['approval_date'], item['djjg'], item['f_body'], item['reasons_cancel'], item['zczb'],
        item['paid_in_capital'], item['ygrs'], item['social_staff_num'], item['industry'], item['Contact_number'],
        item['email'], item['z_body'],))
    db.commit()
    cursor.close()
    db.close()


get_gsxt_holder("64")
