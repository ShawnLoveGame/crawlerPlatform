#coding=utf-8
#2014.12.13
#author@shibin

import json
#import datetime
import sys


def get_part_info(input_fname,output_fname):
	def part_info(line_data):		
		#-----------------------
		uin=json.loads(line_data).get('uin')
		if uin!=None:uin=str(uin)
		return uin
		#-----------------------
		'''
		data_list=line_data.strip().split('\t')
		***=data_list[4][:-4]
		return data_list[1]+"\t"+***
		'''

	input_f=open(input_fname,"r")
	output=open(output_fname,"w")

	part_dict={}
	for line in input_f:	
		if line=="\n":
			continue
		if line=="":
			break
		part=part_info(line)
		if part==None:
			continue
		#if part_dict.has_key(part):
			continue
		output.write(part.strip())
		output.write('\n')
		#part_dict[part]=1
	input_f.close()
	output.close()

def filter_err_line(input_fname,output_fname,err_output=None):
	input_f=open(input_fname,"r+")
	output=open(output_fname,"w+")
	if err_output!=None:
		err=open(err_output,'w+')
	for line in input_f:
		if line=="\n":
			continue
		if line=="":
			break
		try:
			#---------------------------------------------------
			#json_line=line.strip().split('\t')[1]
			#if json.loads(json_line).get("***")==None:
			#	if err_output!=None:
			#		wrr.write(line)
			#	continue
			#output.write(line)


			load_data=json.loads(line)
			#if not load_data.has_key("error_id"):
			output.write(line)
			
		except:
			if err_output!=None:
				err.write(line)
	input_f.close()
	output.close()
	if err_output!=None:
		err.close()

def together_id(input_fname,output_fname):
	def get_decode_data(line):
		#return json.loads(line)
		return line.strip().split('\t')
	def get_id_part(doc):
		return doc[0]
	def get_compare_part(doc):
		return int(doc[1])
		#return datetime.datetime.strptime(time_str,'%Y-%m-%dT%H:%M:%S')
	def compare_change(this_flag,old_flag):
		if this_flag>=old_flag:
			return True
		return None

	id_compare_dict={}
	input_f=open(input_fname,"r+")
	line_count=0
	for line in input_f:
		if line=="\n":
			continue
		if line=="":
			break
		line_count+=1
		this_doc=get_decode_data(line)
		this_id=get_id_part(this_doc)
		this_flag=get_compare_part(this_doc)
		if not id_compare_dict.has_key(this_id):
			id_compare_dict[this_id]=(this_flag,line_count)
			continue
		old_flag=id_compare_dict[this_id][0]
		if compare_change(this_flag,old_flag)==True:
			id_compare_dict[this_id]=(this_flag,line_count)
	input_f.close()
	print len(id_compare_dict.keys()),line_count
	
	lines={}
	for ki in id_compare_dict:
		lines[id_compare_dict[ki][1]]=1

	input_f=open(input_fname,"r")
	output=open(output_fname,"w")
	line_count=0
	for line in input_f:
		if line=="\n":
			continue
		if line=="":
			break
		line_count+=1
		if lines.has_key(line_count):
			output.write(line)
	input_f.close()
	output.close()
	#

def combine_data(input_fname,add_fname,output_fname):
	def get_input_doc(input_line):
		#
		line_list=input_line.split('\t',1)
		item_id=line_list[0]
		json_line=line_list[1]
		doc=json.loads(json_line)
		input_doc={}
		input_doc['id']=item_id
		input_doc['data']=doc
		return input_doc
	def get_add_doc(add_line):
		doc=json.loads(add_line)
		add_doc={}
		add_doc['id']=doc['item_id']
		add_doc['data']=(doc['***'],doc['***'])
		return add_doc
	def make_id_output(input_doc,add_doc):
		item_id=input_doc['id']
		doc=input_doc['data']
		doc['***']=add_doc[1]
		return item_id+'\t'+json.dumps(doc,ensure_ascii=False).encode('utf-8')
	combine_by_id=True
	if combine_by_id:
		id_add={}
		add_f=open(add_fname,'r')
		for line in add_f:
			if line=="\n":
				continue
			if line=="":
				break
			add_doc=get_add_doc(line)
			if add_doc==None:
				continue
			id_add[add_doc['id']]=add_doc['data']
		add_f.close()
		input_f=open(input_fname,'r')
		output=open(output_fname,'w')
		for line in input_f:
			if line=="\n":
				continue
			if line=="":
				break
			input_doc=get_input_doc(line)
			if input_doc==None:
				continue
			add_doc=id_add.get(input_doc['id'])
			if add_doc==None:
				pass
				continue
			new_line=make_id_output(input_doc,add_doc)
			output.write(new_line)
			output.write('\n')
		
		input_f.close()
		output.close()

if __name__ == '__main__':
	if sys.argv[1]=="-part":	
		input_fname=sys.argv[2]
		output_fname=sys.argv[3]
		get_part_info(input_fname,output_fname)
	if sys.argv[1]=="-tgid":
		input_fname=sys.argv[2]
		output_fname=sys.argv[3]
		together_id(input_fname,output_fname)
	if sys.argv[1]=="-ferr":
		input_fname=sys.argv[2]
		output_fname=sys.argv[3]
		err=None
		if len(sys.argv)==5:
			err=sys.argv[4]
		filter_err_line(input_fname,output_fname,err_output=err)
	if sys.argv[1]=="-comb":
		input_fname=sys.argv[2]
		add_fname = sys.argv[3]
		output_fname=sys.argv[4]
		combine_data(input_fname,add_fname,output_fname)
	
