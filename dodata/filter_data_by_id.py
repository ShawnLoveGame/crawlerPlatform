#coding=utf-8
#author@shibin
#2014.11.08
import sys
import json

def get_id_from_id_data(id_data):
	#return id_data.strip()
	#return	id_data.split('\t',1)[0]
	return json.loads(id_data).get('item_id')
	#return 	json.loads(id_data).get('***')
def get_id_from_result_data(result_data):
	return result_data.split('\t',1)[0]
	#return json.loads(result_data).get('***')

def main():
	id_f_name=sys.argv[1]
	result_f_name=sys.argv[2]
	filter_f_name=sys.argv[3]

	id_dict={}
	id_f=open(id_f_name,"r")
	for line in id_f:
		if line=="\n":
			continue
		item_id=get_id_from_id_data(line)
		if item_id==None:
			continue
		id_dict[item_id]=0
	id_f.close()
	got_id_num=len(id_dict.keys())
	print "got_id:",got_id_num

	result_f=open(result_f_name,"r")
	filter_f=open(filter_f_name,"w")
	count=0
	for result_line in result_f:
		count+=1
		if result_line=="\n":
			continue
		r_item_id=get_id_from_result_data(result_line)
		#print r_item_id
		#print result_line
		#raw_input(':')
		if r_item_id==None:
			continue
		if not id_dict.has_key(r_item_id):
			continue
		if id_dict[r_item_id]==1:
			continue
		filter_f.write(result_line)
		id_dict[r_item_id]=1
		if count%1000==1:
			print 'filter 1k data'

	result_f.close()
	filter_f.close()
	got_result_num=sum(id_dict.values())
	print "not get:",got_id_num-got_result_num
	
	if got_id_num==got_result_num:
		return 	
	if len(sys.argv)==4:
		return
		
	no_result_id_fname=sys.argv[4]
	no_result_id_f=open(no_result_id_fname,'w')
	id_f=open(id_f_name,"r")
	for line in id_f:
		if line=="\n":
			continue
		item_id=get_id_from_id_data(line)	
		if item_id==None:
			continue
		if id_dict[item_id]==0:
			no_result_id_f.write(line)
	no_result_id_f.close()
	id_f.close()

if __name__=="__main__":
	main()


