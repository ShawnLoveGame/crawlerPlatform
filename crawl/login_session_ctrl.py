#coding=utf-8
#2014.12.12
#author@shibin

import threading
import requests

import time
import random
def sleep_rand(a,b):
	if type(a)==int and type(b)==int:
		time.sleep(random.randint(a,b))
		return
	time.sleep(random.uniform(a,b))

class login_session_ctrl(object):
	def __init__(self,login_func,max_vote_count=200,max_session_new_time=60*4):
		self.session=requests.Session()
		self.login_mutex = threading.Lock()

		self.login_func=login_func
		self.session_data=None
		
		self.useful=None
		self.session_is_new=True
		self.session_new_time=time.time()
		self.max_session_new_time=max_session_new_time
		self.vote_count=0
		self.max_vote_count=max_vote_count
	def print_log(self,log_data):
		print log_data
	def __login(self):
		try:
			self.session_data=self.login_func(self.session)
			if self.session_data==None:
				return False		
			return True
		except Exception,e:
			print str(e)
			return None
	def login(self):
		#single	login one time
		self.login_mutex.acquire()
		while  1:
			if self.useful==True:
				self.print_log('login already')
				break
			self.useful=self.__login()
			self.print_log('login one time'+str(self.useful))
			break
		self.login_mutex.release()
		return self.useful
	def login_session(self,sleep_time=1):
		while not self.useful:
			self.print_log("here use a while to  try to login")
			if not self.login():
				sleep_rand(sleep_time/2.0,sleep_time*2.0)
	
	def is_useful(self):
		return self.useful
	def copy_session_data(self):
		return self.session_data
	def copy_session(self):
		if self.useful==True:
			return self.session
		self.print_log('not useful, login it')
		self.login_session(sleep_time=5)
		return self.session

	def make_session(self):
		#----------------------------------------
		#check
		if self.session_is_new==True:
			return None
		if self.session_is_new==False:
			self.print_log( 'its time to make new session vote_count:'+str(self.vote_count))
		#check
		#----------------------------------------
		#single	make one time
		self.login_mutex.acquire()
		while  1:
			self.print_log('make new session')
			if self.session_is_new==True:
				self.print_log('new session already')
				break
			self.print_log('init  new session  status')

			self.session=requests.Session()
			self.accesskey=None
			self.useful=None
			self.session_is_new=True
			self.session_new_time=time.time()
			self.vote_count=0
			#this is not a loop break here
			break
		self.login_mutex.release()
		self.print_log('make new session true')

	def make_new(self):
		self.login_mutex.acquire()
		if time.time()-self.session_new_time>self.max_session_new_time:
			self.session_is_new=False
		self.login_mutex.release()
		self.make_session()
		return True
	def vote_new(self,count=1):
		self.login_mutex.acquire()
		self.vote_count+=count
		if self.vote_count+count>self.max_vote_count:
			self.session_is_new=False
		self.login_mutex.release()
		self.make_session()
		return  True
#-------------------------------------------------