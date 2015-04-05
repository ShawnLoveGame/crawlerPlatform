#coding=utf-8
#2014.12.12
#author@shibin
import threading
import time
import random

def sleep_rand(a,b):
	if type(a)==int and type(b)==int:
		time.sleep(random.randint(a,b))
		return
	time.sleep(random.uniform(a,b))

def threads_all_died(threads):
	return filter(lambda x :x,[t.isAlive() for t in threads])==[]

def exit_threads(threads):
	for t in threads:
		t.set_exit()

class two_queue_thread(threading.Thread):
	def __init__(self, input_queue,output_queue,run_each_input,check_each_output,arg_data=None):
		threading.Thread.__init__(self)
		self.input_queue=input_queue
		self.output_queue=output_queue
		self.run_each_input=run_each_input
		self.check_each_output=check_each_output
		self.arg_data=arg_data
		self.exit=False
	def set_exit(self):self.exit=True

	def get_satus(self):
		print "input:%d output:%d"%(self.input_queue.qsize(),self.output_queue.qsize())
	def run(self):

		while 1:
			if self.exit:
				break
			if self.input_queue.qsize()==0:
				self.get_satus()
				sleep_rand(1/0.2,2*2.0)
			try:
				doc=self.input_queue.get_nowait()
			except:
				continue
			#print self.getName(),"got one to run"
			Isture,result=self.run_each_input(doc,arg_data=self.arg_data)	
			if Isture==None:
				continue
			check,check_output=self.check_each_output(doc,Isture,result,arg_data=self.arg_data)
			if check==None:
				continue
			if check== False:
				self.input_queue.put(check_output)
			if check== True:
				self.output_queue.put(check_output)
		print "%s exit this threads"%(self.getName())

