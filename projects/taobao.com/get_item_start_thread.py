#coding=utf-8
#author@shibin
#2016.07.13

from queue_common import sleep_rand
#from queue_common import threads_all_died
#from queue_common import exit_threads
from queue_common import default_check as check
from queue_common import read_tool
from queue_common import write_tool
#from queue_common import thread_tool
#from queue_common import two_queue_thread
from queue_common import main_tool

from get_item_start import get_detail
from get_item_start import get_start

import sys

def run(doc,**kwargs):
    item_id = doc
    text = get_detail(item_id)
    if text == None:
        return False,None
    start = get_start(text)
    if start == False:
        sleep_rand(1*60,2*60)
        return False,None
    if start == None:
        sleep_rand(0,30)
        return False,None
    return True,start


def readline(line,inq=None,**kwargs):
    item_id = line.strip()
    if inq != None:
        inq.put(item_id)
        return True
    return False


def writeout(out,fout,inq=None,**kwargs):
    doc, result = out
    item_id = doc
    start = result

    fout.write('{}\t{}\n'.format(item_id,start))
    return True


def main(fin,fout,th_ct):
    reader = read_tool(fin, readline)
    writer = write_tool(fout, writeout)

    main_tool(reader, run, check, writer,th_ct=th_ct)


if __name__ == '__main__':
    fin = open(sys.argv[1],'r')
    fout = open(sys.argv[2],'w')
    th_ct = 10
    if len(sys.argv) == 4:
        th_ct = int(sys.argv[3])

    main(fin,fout,th_ct)
