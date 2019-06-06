from crawlerDocuments.get_datebase import *
import json
import datetime
from fetchDataBase import *


def deal_each_data(gsxt_base, tyc_base):
    item = {}

    item['Enterprise_name'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'entName'),
                                                            databaseTool.is_field_dict(tyc_base, 'com_name'))

    item['Enterprise_tyshxydm'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'uniscId'),
                                                                databaseTool.is_field_dict(tyc_base, 'creditCode'))

    item['Legalrepresentative'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'person_name'),
                                                                databaseTool.is_field_dict(tyc_base,
                                                                                           'legalPersonName'))

    item['Enterprise_zzjgdm'] = databaseTool.collection_field(None,
                                                              databaseTool.is_field_dict(tyc_base, 'orgNumber'))

    item['Enterprise_gszch'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'register_num'),
                                                             databaseTool.is_field_dict(tyc_base, 'regNumber'))

    item['rtime'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'estDate'),
                                                  databaseTool.is_field_dict(tyc_base, 'estiblishTime'))

    item['registered_address'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'dom'),
                                                               databaseTool.is_field_dict(tyc_base, 'regLocation'))

    item['gslx'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'entType'),
                                                 databaseTool.is_field_dict(tyc_base, 'companyOrgType'))

    item['jyzt'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'regState'),
                                                 databaseTool.is_field_dict(tyc_base, 'regStatus'))

    item['op_from'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'opFrom'),
                                                    databaseTool.is_field_dict(tyc_base, 'fromTime'))

    item['op_to'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'opTo'), None)

    item['approval_date'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'apprDate'),
                                                          databaseTool.is_field_dict(tyc_base, 'approvedTime'))

    item['djjg'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'regOrg'),
                                                 databaseTool.is_field_dict(tyc_base, 'regInstitute'))

    item['f_body'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'opScope'),
                                                   databaseTool.is_field_dict(tyc_base, 'businessScope'))

    item['reasons_cancel'] = databaseTool.collection_field(databaseTool.is_field_dict(gsxt_base, 'cancel_reason'),
                                                           None)

    item['zczb'] = databaseTool.collection_field(None,
                                                 databaseTool.is_field_dict(tyc_base, 'regCapital'))

    item['paid_in_capital'] = databaseTool.collection_field(None,
                                                            databaseTool.is_field_dict(tyc_base, 'actualCapital'))

    item['ygrs'] = databaseTool.collection_field(None,
                                                 databaseTool.is_field_dict(tyc_base, 'staffNumRange'))

    item['social_staff_num'] = databaseTool.collection_field(None,
                                                             databaseTool.is_field_dict(tyc_base, 'socialStaffNum'))

    item['industry'] = databaseTool.collection_field(None,
                                                     databaseTool.is_field_dict(tyc_base, 'industry'))

    item['Contact_number'] = databaseTool.collection_field(None,
                                                           databaseTool.is_field_dict(tyc_base, 'phoneNumber'))

    item['email'] = databaseTool.collection_field(None, databaseTool.is_field_dict(tyc_base, 'email'))

    item['z_body'] = databaseTool.collection_field(None,
                                                   databaseTool.is_field_dict(tyc_base, 'baseInfo'))
    item['source_update_time'] = databaseTool.collection_field(None,
                                                               databaseTool.is_field_dict(tyc_base, 'ty_update_time'))
    item['local_update_time'] = datetime.datetime.now()

    print(item)
    if item['Enterprise_name']:
        insert_base_info(item)
        main_id = select_main_id(databaseTool.unify_character(item['Enterprise_name']))
        # 整合股东信息
        aggregate_holder_info(main_id, databaseTool.is_field_dict(gsxt_base, 'id'),
                              databaseTool.is_field_dict(tyc_base, 'id'))
        # 整合分支机构信息
        aggregate_branch_info(main_id, databaseTool.is_field_dict(gsxt_base, 'id'),
                              databaseTool.is_field_dict(tyc_base, 'id'))


def aggregate_branch_info(main_id, gsxt_id, ty_id):
    c_list = []
    ty_list = get_tyc_branch(ty_id)
    gx_list = get_gx_branch(gsxt_id)
    print("ty_branch_list: ", ty_list)
    print("gx_branch_list: ", gx_list)
    if gx_list:
        for branch in gx_list:
            item = {}
            item['branch_name'] = branch['brName']
            item['credit_code'] = branch['uniscId']
            item['Enterprise_gszch'] = branch['regNo']
            item['reg_authority'] = branch['regOrg']
            item['legal_person'] = None
            item['industry'] = None
            item['estiblish_date'] = None
            item['business_state'] = None
            c_list = databaseTool.collection_list_field(c_list, item, "branch_name")
    if ty_list:
        for branch in ty_list:
            item = {}
            item['branch_name'] = branch['com_name']
            item['credit_code'] = None
            item['Enterprise_gszch'] = None
            item['reg_authority'] = None
            item['legal_person'] = branch['legalPersonName']
            item['industry'] = branch['category']
            item['estiblish_date'] = branch['estiblishTime']
            item['business_state'] = branch['regStatus']
            c_list = databaseTool.collection_list_field(c_list, item, "branch_name")
    for item in c_list:
        insert_branch_info(main_id, item)


def aggregate_holder_info(main_id, gsxt_id, ty_id):
    c_list = []
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
    if gx_holder_list:
        for holder in gx_holder_list:
            item = {}
            item['shareholder'] = holder["inv_name"]
            item['shareholder_type'] = holder["invType"]
            item['blic_type'] = holder["blicType"]
            item['blic_number'] = holder["bLicNo"]
            item['ent_type'] = holder["respForm"]
            item['con_capital'] = holder["subConAm"]
            item['con_capital_date'] = holder["conDate"]
            item['con_paid_in_capital'] = holder["acConAm"]
            item['paid_in_capital_date'] = holder["conDate"]
            item['share_ratio'] = None
            print("gx_holder_item : ", item)
            c_list = databaseTool.collection_list_field(c_list, item, "shareholder")
    if tyc_holder_list:
        for holder in tyc_holder_list:
            item = {}
            item['shareholder'] = holder["person_name"]
            item['shareholder_type'] = None
            item['blic_type'] = None
            item['blic_number'] = None
            item['ent_type'] = None
            item['con_capital'] = holder["amomon"]
            item['con_capital_date'] = holder["h_time"]
            item['con_paid_in_capital'] = None
            item['paid_in_capital_date'] = None
            item['share_ratio'] = holder["percent"]
            print("tyc_holder_item : ", item)
            c_list = databaseTool.collection_list_field(c_list, item, "shareholder")
    print(c_list)
    for item in c_list:
        insert_holder_info(main_id, item)

# get_gsxt_holder("64")
# sear = {"company": "山东泉林集团有限公司"}
# g, t = get_each_data(sear)
# deal_each_data(g, t)
