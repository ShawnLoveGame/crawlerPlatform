#coding=utf-8
#2015/04/16
#author@shibin

#
#
import sys
from optparse import OptionParser 


def getoptparse():
	parser = OptionParser() 
	parser.add_option("-A","--source-A",action="store",
		dest="soureApath", 
		default="", 
		help="soureApath")
	parser.add_option("-B","--source-B",action="store",
		dest="soureBpath", 
		default="", 
		help="soureBpath")
	parser.add_option("-x","--xor",action="store",
		dest="xorpath", 
		default="", 
		help="xorpath")
	parser.add_option("-a","--and",action="store",
		dest="andpath", 
		default="", 
		help="andpath")
	parser.add_option("--A-B",action="store",
		dest="A_Bpath", 
		default="", 
		help="A_Bpath")
	parser.add_option("--B-A",action="store",
		dest="B_Apath", 
		default="", 
		help="B_Apath")
	return parser

def read_A(f):
	for line in f:
		return False,int(line.strip())
	return True,None

def read_B(f):
	for line in f:
		return False,int(line.strip())
	return True,None

def compare(a,b):
	if a==b:
		return None
	return a<b

def write(result,write_types,output_types,outputs):
	for i in range(4):
		if write_types[i]==True:
			if output_types[i]==True:
				outputs[i].write(result)

def write_Asmall(a,output_types,outputs):
	result=str(a)+'\n'
	write_types=(True,None,True,None)
	write(result,write_types,output_types,outputs)

def write_Bsmall(b,output_types,outputs):
	result=str(b)+'\n'
	write_types=(True,None,None,True)
	write(result,write_types,output_types,outputs)

def write_equal(a,output_types,outputs):
	#means equal
	result=str(a)+'\n'
	write_types=(None,True,None,None)
	write(result,write_types,output_types,outputs)


def main(f_a,f_b,output_types,f_outputs):
	Af=open(f_a,'r')
	Bf=open(f_b,'r')
	outputs=[]
	for i in range(4):
		if output_types[i]==True:
			outputs.append(open(f_outputs[i],'w'))
		else:
			outputs.append(None)

	a_close=False
	b_close=False
	a=None
	b=None
	read_a=True	
	read_b=True

	ct=0
	while 1:
		if a_close!=None and read_a:
			result=read_A(Af)
			a_close,a=read_A(Af)
			if a_close==True:
				Af.close()
				a_close=None
		if b_close!=None and read_b:
			b_close,b=read_B(Bf)
			if b_close==True:
				Bf.close()
				b_close=None


		if a_close==None and b_close==None:
			#all--read---a,b-is None
			break
		if a_close==False and b_close==None:
			#means--b is close
			write_Asmall(a,output_types,outputs)
			read_a=True
			read_b=False
			continue
		if a_close==None and b_close==False:
			#means--a is close
			write_Bsmall(b,output_types,outputs)
			read_a=False
			read_b=True
			continue

		if a_close==False and b_close==False:
			#means a & b not None
			"""
			#test
			if a==1670512627:
				print 'b',b
				raw_input()
			if b==1670512627:
				print 'a',a
				raw_input()
			if a==1215854130:
				print 'b',b
				raw_input()
			if b==1215854130:
				print 'a',a
				raw_input()
			"""
			a_small_b=compare(a,b)
			ct+=1
			if ct%100000==0:
				print 'try 100k:',ct
			if a_small_b==None:
				write_equal(a,output_types,outputs)
				read_a=True
				read_b=True

			if a_small_b==True:
				write_Asmall(a,output_types,outputs)
				#read next a compare to this b 
				read_a=True
				read_b=False
			if a_small_b==False:
				write_Bsmall(b,output_types,outputs)
				#read next b compare to this a
				read_a=False
				read_b=True

	for i in range(4):
		if output_types[i]==True:
			outputs[i].close()


if __name__=="__main__":
	parser=getoptparse()
	(options, args) = parser.parse_args()
	f_a=options.soureApath
	f_b=options.soureBpath

	output_types=[]
	f_outputs=[]
	#xor
	if options.xorpath!="":
		output_types.append(True)
		f_outputs.append(options.xorpath)
	else:
		output_types.append(None)
		f_outputs.append(None)

	#and
	if options.andpath!="":
		output_types.append(True)
		f_outputs.append(options.andpath)
	else:
		output_types.append(None)
		f_outputs.append(None)

	#A-B
	if options.A_Bpath!="":
		output_types.append(True)
		f_outputs.append(options.A_Bpath)
	else:
		output_types.append(None)
		f_outputs.append(None)

	#B-A
	if options.B_Apath!="":
		output_types.append(True)
		f_outputs.append(options.B_Apath)
	else:
		output_types.append(None)
		f_outputs.append(None)

	main(f_a,f_b,output_types,f_outputs)
