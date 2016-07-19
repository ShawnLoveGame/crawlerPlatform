#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse

import json
import sys

# set A,set B, give  A - B 
# do not need sorted, It use the memory
# all string should be keep as unicode


def get_id_from_A(line_data):
    return line_data.strip()
    #return json.loads(line_data).get('id')
    #return json.loads(line_data)['weibo']
    #return line_data.strip().decode('utf-8')
    #return json.loads(line_data)['name']
    #return json.loads(line_data).get('item_id')
    #return json.loads(line_data).get('auctionId')
    #return json.loads(line_data).get('pi')
    #return json.loads(line_data).get('company_id')
    #return json.loads(line_data).get('search_unicode')
    #return json.loads(line_data).get('unique')
    #return json.loads(line_data).get('KeyNo')
    #return line_data.split('\t',1)[0]
    #return line_data.strip().split('\t',1)[1]
    #return line_data.split('\t',1)[0]
    #return json.loads(line_data).get('shop_id')
    #return json.loads(line_data).get('item_info').get('item_id')
    #return json.loads(line_data).get('item_info').get('category_id')


def get_id_from_B(line_data):
    return line_data.strip()
    #return line_data.strip().decode('utf-8')
    #return line_data.strip().split('\t')[0]
    #return line_data.strip().split('\t',1)[0]
    #return line_data.strip().split('\t',1)[1]
    #return line_data.strip()[-32:]
    #return json.loads(line_data).get('uid')
    #return json.loads(line_data).get('key')
    #return json.loads(line_data).get('urltail')
    #return json.loads(line_data).get('shop_id')
    #return json.loads(line_data).get('name')
    #return json.loads(line_data).get('item_info').get('item_id')
    #return json.loads(line_data).get('item_info').get('category_id')
    #return json.loads(line_data).get('company_id')[-32:]
    #return json.loads(line_data).get('company_id')
    #return json.loads(line_data).get('name')
    #return json.loads(line_data).get('unique')
    #return json.loads(line_data).get('item_id')
    #return json.loads(line_data).get('search_unicode')
    #return json.loads(line_data)['weibo']
    #return json.loads(line_data).get('user_id')
    #return json.loads(line_data).get('brand_id')
    #return json.loads(line_data).get('pi')
    #return json.loads(line_data).get('urltail')
    #uin=json.loads(line_data).get('uin')
    #if uin!=None: return str(uin)


id_dict = {}

A_file = open(sys.argv[1], 'r')
B_file = open(sys.argv[2], 'r')
output = open(sys.argv[3], 'w')

#default A is not small
Asmall = False
#Asmall=True

if Asmall:
    print('set B might too big')

    for line_A in A_file:
        if line_A == "\n":
            continue
        _id = get_id_from_A(line_A)
        id_dict[_id] = 0
    A_file.close()

    print('A _id count is {}'.format(len(id_dict)))

    for line_B in B_file:
        if line_B == "\n":
            continue
        _id = get_id_from_B(line_B)
        if _id in id_dict:
            id_dict[_id] = 1
    B_file.close()

    count = 0
    A_file = open(sys.argv[1], 'r')
    for line_A in A_file:
        if line_A == "\n":
            continue
        _id = get_id_from_A(line_A)
        if id_dict[_id] == 1:
            continue        
        output.write(line_A)
        count += 1
    print('A in B is {}'.format(count))

    A_file.close()
    output.close()

if not Asmall:
    print('set A is too big')
    for line_B in B_file:
        if line_B == "\n":
            continue
        _id = get_id_from_B(line_B)
        id_dict[_id] = 1
    B_file.close()

    print('B _id count is:{}'.format(len(id_dict)))
    count = 0
    for line_A in A_file:
        if line_A == "\n":
            continue
        _id = get_id_from_A(line_A)
        if _id in id_dict:
            continue
        output.write(line_A)
        count += 1
    print('A in B is {}'.format(count))
    A_file.close()
    output.close()
