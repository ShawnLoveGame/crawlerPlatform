#--------------------------------------------------------
#this is just a test to simulate web error queue 
#--------------------------------------------------------
from queue_common import two_queue_thread,exit_threads,threads_all_died,sleep_rand
import Queue
import random

def run_each_num(doc,arg_data=None):
	if type(doc)!=int:
		return None,None
	sleep_rand(0,1.0)
	if random.randint(0,10)==0:
		return False,0
	return True,doc*doc

def check_each_output(doc,Isture,result,arg_data=None):
	if Isture==False:
		print "try again this one",doc
		return False,doc
	#if doc["trycount"]>4:
	#	return False,doc
	return True,result

def test_main():

	input_queue=Queue.Queue()
	output_queue=Queue.Queue()

	for i in range(50):
		input_queue.put(i)

	threads=[]
	for i in range(5):
		t=two_queue_thread(input_queue,output_queue,run_each_num,check_each_output)
		threads.append(t)
		t.start()

	for i in range(10):
		sleep_rand(2,5)
		threads[0].get_satus()
		if input_queue.qsize()==0:
			break

	print "add some one"
	for i in range(50,100):
		input_queue.put(i)

	result=0
	while 1:

		if input_queue.qsize()==0:
			exit_threads(threads)
			if threads_all_died(threads):
				break
		sleep_rand(1,1)
		threads[0].get_satus()
		while 1:
			try:
				one_result=output_queue.get_nowait()
			except:
				break
			result+=one_result
	true_result=0
	for i in range(0,100):
		true_result+=i*i
	print result,true_result

if __name__=="__main__":
	print "this is a test"
	test_main()
