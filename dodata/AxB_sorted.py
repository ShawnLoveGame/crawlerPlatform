#coding=utf-8
#2015/04/16
#author@shibin

#
#import optparse???
import sys


def read_A(f):
	for line in f:
		#return False,line.strip()
		return False,int(line.strip())
	return True,None

def read_B(f):
	for line in f:
		#return False,line.strip()
		return False,int(line.strip())
	return True,None

def make_Aresult(a):
	return str(a)+'\n'
def make_Bresult(b):
	return str(b)+'\n'

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
	result=make_Aresult(a)
	write_types=(True,None,True,None)
	write(result,write_types,output_types,outputs)

def write_Bsmall(b,output_types,outputs):
	result=make_Bresult(b)
	write_types=(True,None,None,True)
	write(result,write_types,output_types,outputs)

def write_equal(a,output_types,outputs):
	#means equal
	result=make_Aresult(a)
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
	f_a=sys.argv[2]
	f_b=sys.argv[3]
	#--------------
	#wait me to add optparse
	#.......
	if sys.argv[1]=="--xor":
		#异或
		#A xor B
		xor_out=sys.argv[4]
		output_types=(True,None,None,None)
		f_outputs=(xor_out,None,None,None)
	if sys.argv[1]=="--and":
		#A and B
		and_out=sys.argv[4]
		output_types=(None,True,None,None)
		f_outputs=(None,and_out,None,None)
	if sys.argv[1]=="--A-B":
		#A-B		
		xor_aout=sys.argv[4]
		output_types=(None,None,True,None)
		f_outputs=(None,None,xor_aout,None)
	if sys.argv[1]=="--B-A":
		#B-A
		xor_bout=sys.argv[4]
		output_types=(None,None,None,True)
		f_outputs=(None,None,None,xor_bout)
	if sys.argv[1]=="--xor--and":
		#xor and
		xor_out=sys.argv[4]
		and_out=sys.argv[5]
		output_types=(True,True,None,None)
		f_outputs=(xor_out,and_out,None,None)
	if sys.argv[1]=="--xor--B-A--A-B":
		xor_aout=sys.argv[4]
		xor_bout=sys.argv[5]
		output_types=(None,None,True,True)
		f_outputs=(None,None,xor_aout,xor_bout)
	if sys.argv[1]=="--xor--B-A--A-B--and":
		xor_aout=sys.argv[4]
		xor_bout=sys.argv[5]
		and_out=sys.argv[6]
		output_types=(None,True,True,True)
		f_outputs=(None,xor_aout,xor_bout,and_out)

	main(f_a,f_b,output_types,f_outputs)
