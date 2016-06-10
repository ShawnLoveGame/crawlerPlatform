#!/usr/bin/env python2.7
#coding=utf-8
#author@shibin
import sys
import json
#
#all unicode
#
# find A not in B   give the rest part of A
def get_id_from_A(line_data):
	#return json.loads(line_data)['weibo']
	#return line_data.strip()
	#return json.loads(line_data).get('id')
	#return line_data.strip().decode('utf-8')
	#return json.loads(line_data)['name']
	#return json.loads(line_data).get('item_id')
	#return json.loads(line_data).get('auctionId')
	#return json.loads(line_data).get('pi')
	#return json.loads(line_data).get('company_id')
	#return json.loads(line_data).get('search_unicode')
	#return json.loads(line_data).get('unique')
	#return json.loads(line_data).get('KeyNo')
	return line_data.split('\t',1)[0]
	#return line_data.strip().split('\t',1)[1]
	#return line_data.split('\t',1)[0]
	#return json.loads(line_data).get('shop_id')
	#return json.loads(line_data).get('item_info').get('item_id')
	#return json.loads(line_data).get('item_info').get('category_id')

def get_id_from_B(line_data):
	#return line_data.strip().decode('utf-8')
	#return json.loads(line_data).get('item_id')
	#return json.loads(line_data).get('search_unicode')
	#return json.loads(line_data)['weibo']
	#return json.loads(line_data).get('user_id')
	#return json.loads(line_data).get('brand_id')
	#return json.loads(line_data).get('pi')
	#return json.loads(line_data).get('urltail')
	#return line_data.strip()
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
	#uin=json.loads(line_data).get('uin')
	#if uin!=None:uin=str(uin)
	#return uin
	#return line_data.strip().split('\t')[0]
	return line_data.strip().split('\t',1)[0]
	#return line_data.strip().split('\t',1)[1]
	#return line_data.strip()
	#return line_data.strip()[-32:]

# find A not in B   give the rest part of A
#like A=[1,2,4,5]
#B=[3,4,5,6,7,8,9,10]
#the file give 1/2 the same part of A 
id_dict={}
A_file=open(sys.argv[1],'r')
B_file=open(sys.argv[2],'r')
output=open(sys.argv[3],'w')
#one A is small 
Asmall=False
Asmall=True
if Asmall:
	print 'b is too big'
	for line_A in A_file:
		if line_A=="\n":
			continue
		item_id=get_id_from_A(line_A)
		id_dict[item_id]=0		
	A_file.close()
	print 'A is ',len(id_dict.keys())
	for line_B in B_file:
		if line_B=="\n":
			continue
		item_id=get_id_from_B(line_B)
		if item_id in id_dict:
			id_dict[item_id]=1
	B_file.close()

	print 'A in B',sum(id_dict.values())

	A_file=open(sys.argv[1],'r')
	for line_A in A_file:
		if line_A=="\n":
			continue
		item_id=get_id_from_A(line_A)
		if id_dict[item_id]==1:
			continue
		output.write(line_A)
	A_file.close()
	output.close()

if not Asmall:
	print 'A is too big'
	for line_B in B_file:
		if line_B=="\n":
			continue			
		item_id=get_id_from_B(line_B)		
		id_dict[item_id]=1
	B_file.close()

	print 'B is ',len(id_dict.keys())

	for line_A in A_file:
		if line_A=="\n":
			continue
		item_id=get_id_from_A(line_A)
		if item_id in id_dict:
			continue
		output.write(line_A)
	A_file.close()
	output.close()
