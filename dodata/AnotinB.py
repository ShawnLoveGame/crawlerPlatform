#coding=utf-8
#author@shibin
import sys
import json
#
#all unicode
#
# find A not in B   give the rest part of A
def get_id_from_A(line_data):
	return line_data.strip()
	#return line_data.strip().decode('utf-8')
	#return json.loads(line_data).get('item_id')
	#return line_data.split('\t',1)[0]
	#return json.loads(line_data).get('shop_id')
	#return line_data.split('\t',1)[0]
def get_id_from_B(line_data):
	#return line_data.strip().decode('utf-8')
	#return json.loads(line_data).get('item_id')
	#return json.loads(line_data).get('user_id')
	#return line_data.strip()
	return json.loads(line_data).get('key')
	#return line_data.strip()
	#uin=json.loads(line_data).get('uin')
	#if uin!=None:
		#uin=str(uin)
		#return uin
	#return line_data.strip()
	#return line_data.strip()
	#return json.loads(line_data).get('shop_id')
	#return line_data.strip()
	#return line_data.strip().split('\t')[0]
	#return json.loads(line_data).get('key')
# find A not in B   give the rest part of A
#like A=[1,2,4,5]
#B=[3,4,5,6,7,8,9,10]
#the file give 1/2 the same part of A 

#one A is small 
#Asmall=True
Asmall=False
if sys.argv[1]=="Abig":
	Asmall=False
if sys.argv[1]=="Bbig":
	Asmall=True

id_dict={}
A_file=open(sys.argv[2],'r')
B_file=open(sys.argv[3],'r')
output=open(sys.argv[4],'w')

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
		if id_dict.has_key(item_id):
			id_dict[item_id]=1
	B_file.close()

	print 'A in B',sum(id_dict.values())

	A_file=open(sys.argv[1],'r+')
	for line_A in A_file:
		if line_A=="\n":
			continue
		item_id=get_id_from_A(line_A)
		# here can change 1 to 0 to get what is in B
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
		if id_dict.has_key(item_id):
			continue
		output.write(line_A)
	A_file.close()
	output.close()

