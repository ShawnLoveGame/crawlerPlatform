#!/usr/bin/env python2.7
#coding=utf-8
#2015/04/16
#author@shibin

import argparse

'''
sorted:file A  just like set A
sorted:file B  just like set B
'''

#read,(compare,line) from A
def read_A(f):
	for line in f:
		return False,(int(line.strip()),line)
	return True,None

#read,(compare,line) from B
def read_B(f):
	for line in f:
		return False,(int(line.strip()),line)
	return True,None

#default cmp or other cmpare func
def compare(cmp_a,cmp_b):
	return cmp(cmp_a,cmp_b)

#AND,OR,XOR,A-B,B-A
#:write a
A_writes = [False,True,True,True,False]
#:write b
B_writes = [False,True,True,False,True]
#:write equal
Equal_writes  = [True,True,False,False,False]

ASC = 'ASC'
DESC = 'DESC'
directs = [ASC,DESC]


def write_out(out,writes,outputs):
	for i in range(len(writes)):
		if writes[i] == True and outputs[i] != None:
			outputs[i].write(out)


class  SoredFile(object):
	"""the sorted:file status"""
	def __init__(self,f,read_f):
		self.f = f
		self.read_f = read_f
		self.closed = False
		#data == (compare,line)
		self.data = None
		self._need_read = True
		self.count = 0

	def need_read(self):
		self._need_read = True

	def get_line(self):
		if self.data != None:
			return self.data[1]
		raise Exception("no line data has been read")

	def get_compare(self):
		if self.data != None:
			return self.data[1]
		raise Exception("no line data has been read")

	def read(self):
		#只有 未读完关闭、并需要读、才去读
		if self.closed == False and self._need_read == True:
			close,data = self.read_f(self.f)
			self.closed = close
			self._need_read = False		
			if close == True:
				self.f.close()
			else:
				_cmp,line = data
			self.data = data
		return self.closed


def operat(f_A,f_B,outputs,direct = ASC):
	sf_A = SoredFile(f_A,read_A)
	sf_B = SoredFile(f_B,read_B)

	while True:

		close_A = sf_A.read()
		close_B = sf_B.read()

		if not close_A and not close_B:
			AcmpB = compare(sf_A.get_compare(),sf_B.get_compare())

			if AcmpB == 0:
				writes = Equal_writes
			else:
				if (AcmpB == -1 and direct == ASC) or \
					(AcmpB == 1 and direct == DESC):
					writes = A_writes
				else:
					writes = B_writes
		elif not close_A and close_B:
			writes = A_writes
		elif close_A and not close_B:
			writes = B_writes
		elif close_A and close_B:
			break


		if writes == A_writes:
			out = sf_A.get_line()
		else:
			out = sf_B.get_line()

		write_out(out,writes,outputs)

		if writes == A_writes:
			sf_A.need_read()
		elif writes == B_writes:
			sf_B.need_read()
		elif writes == Equal_writes:
			sf_A.need_read()
			sf_B.need_read()





if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('A',help='sorted:file A as set A')
	parser.add_argument('B',help='sorted:file B as set B')

	parser.add_argument('-x','--xor',help='sorted:file A ^ sorted:file B',action='store')
	parser.add_argument('-a','--AND','--and',help='sorted:file A & sorted:file B',action='store')
	parser.add_argument('--A_B',help='sorted:file A - sorted:file B',action='store')
	parser.add_argument('--B_A',help='sorted:file B - sorted:file A',action='store')
	parser.add_argument('-o','--OR','--or',help='set A | set B',action='store')	
	parser.add_argument('-d','--direct',help='direct must be ASC or DESC',default=ASC,choices=[ASC,DESC],action='store')
	args = parser.parse_args()

	f_a = open(args.A,'r')
	f_b = open(args.B,'r')

	direct = args.direct.upper()
	if direct not in directs:
		print('direct error')
		exit()

	outputs = [args.AND,args.OR,args.xor,args.A_B,args.B_A]
	for i in range(len(outputs)):
		f = outputs[i]
		if f != None:
			outputs[i] = open(f,'w')

	operat(f_a,f_b,outputs,direct)
	for output in outputs:
		if output != None:
			output.close()