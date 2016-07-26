#coding=utf-8
#author@shibin
#2016.07.26

from queue_common import sleep_rand
#from queue_common import threads_all_died
#from queue_common import exit_threads
from queue_common import default_check as check
from queue_common import read_tool
from queue_common import write_tool
#from queue_common import thread_tool
#from queue_common import two_queue_thread
from queue_common import main_tool

from get_baseinfo import get_info


import json
import sys


def run(doc,**kwargs):
    data = doc
    info = get_info(data)
    if info == None:
        return False,None
    return True,info


#id 
#accpNo
#regNo
def readline(line,inq = None,**kwargs):
    doc = json.loads(line)
    if inq != None:
        inq.put(doc)
        return True
    return False


def writeout(out, fout, inq=None,**kwargs):
    data,info = out
    info['rawinput'] = data
    fout.write(json.dumps(info,ensure_ascii=False).encode('utf-8'))
    fout.write('\n')
    return True


def main(fin,fout,th_ct=10,**kwargs):
    reader = read_tool(fin, readline)
    writer = write_tool(fout, writeout)
    main_tool(reader, run, check, writer)


if __name__ == '__main__':
    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    th_ct = 10
    if len(sys.argv) == 4:
        th_ct = int(sys.argv[3])
    main(fin,fout,th_ct=th_ct)




