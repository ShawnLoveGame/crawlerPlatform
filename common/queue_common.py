#coding=utf-8
#2014.12.12
#author@shibin

from __future__ import print_function
from threading import Thread
from Queue import Empty, Queue
import random
import time


def sleep_rand(a, b):
    if type(a) == int and type(b) == int:
        time.sleep(random.randint(a, b))
    else:
        time.sleep(random.uniform(a, b))


def threads_all_died(threads):
    return filter(lambda x: x, [t.isAlive() for t in threads]) == []


def exit_threads(threads):
    for t in threads:
        t.exit()


def default_check(doc, istrue, result, **kwargs):
    if istrue:
        return istrue, (doc, result)
    return istrue, doc


def read_tool(fin, readlinef):
    local = {}
    local['fin'] = fin
    local['func'] = readlinef
    local['closed'] = None

    #the count put in the ``inq``
    local['put_ct'] = 0

    def reader(line_count=1000, *args, **kwargs):
        fin = local['fin']
        func = local['func']

        #means is file read finished && closed
        closed = local['closed']

        if not closed:
            put = 0
            for line in fin:
                count = func(line, *args, **kwargs)
                if count == None:
                    count = 1
                if type(count) == int:
                    put += count
                if put == line_count:
                    closed = False
                    break
            local['put_ct'] += put

            if closed == None:
                #fin.close()
                closed = True
                local['closed'] = True

        put_ct = local['put_ct']
        return closed, put_ct

    return reader


#ex: 10 lines --> one ``doc``
def read_fin_tool(fin, readfinf):
    local = {}
    local['fin'] = fin
    local['func'] = readfinf
    local['closed'] = None
    local['put_ct'] = 0

    def reader(read_count=1000, *args, **kwargs):
        fin = local['fin']
        func = local['func']
        closed = local['closed']
        if not closed:
            put = 0
            while 1:
                count = func(fin, *args, **kwargs)
                if count == None:
                    count = 1
                elif count == False:
                    closed = None
                    break
                if type(count) == int:
                    put += count
                if put == read_count:
                    closed = False
                    break
            local['put_ct'] += put

            if closed == None:
                fin.close()
                closed = True
                local['closed'] = True

        put_ct = local['put_ct']
        return closed, put_ct

    return reader


def write_tool(fout, writef):
    local = {}
    local['fout'] = fout
    local['func'] = writef

    #``put_ct``
    local['get_ct'] = 0

    def writer(out, inq=None, **kwargs):
        fout = local['fout']
        func = local['func']
        get = 0

        status = func(out, fout, inq=inq, **kwargs)
        if status == None or status == True:
            get = 1
        if type(status) == int:
            get == status

        local['get_ct'] += get

        return local['get_ct']

    return writer


def thread_tool(run, check, inq, outq, th_ct, **kwargs):
    threads = []
    for i in range(th_ct):
        t = two_queue_thread(run, check, inq, outq, **kwargs)
        t.start()
        threads.append(t)

    return threads


def main_tool(reader,run,check,writer,th_ct=3,min_qsize=3000,log=print,**kwargs):
    inq = Queue()
    outq = Queue()

    threads = thread_tool(run, check, inq, outq, th_ct, **kwargs)

    closed, put_ct = reader(inq=inq, **kwargs)
    get_ct = 0

    while True:

        #input
        if not closed:
            if inq.qsize() < min_qsize:
                closed, put_ct = reader(inq=inq, **kwargs)
        if closed:
            if inq.qsize() == 0 and put_ct == get_ct:
                exit_threads(threads)
            if threads_all_died(threads):
                break

        #status
        sleep_rand(2, 2)
        status = 'put:{} get:{} inq:{} outq:{}'.format(
            put_ct, get_ct, inq.qsize(), outq.qsize())
        log(status)

        #output
        while True:
            try:
                out = outq.get_nowait()
                get_ct = writer(out, inq=inq, **kwargs)
            except Empty:
                break


class two_queue_thread(Thread):
    def __init__(self, run, check, inq, outq, log=print, **kwargs):
        Thread.__init__(self)
        self.inq = inq
        self.outq = outq
        self._run = run
        self.check = check
        self.kwargs = kwargs
        self._exit = False

        self._log = log

    def exit(self):
        self._exit = True

    def run(self):

        while 1:
            if self._exit == True:
                break
            if self.inq.qsize() == 0:
                sleep_rand(1.0, 5.0)

            try:
                doc = self.inq.get_nowait()
            except Empty:
                continue

            istrue, result = self._run(doc, **self.kwargs)
            #pass
            if istrue == None:
                continue
            status, out = self.check(doc, istrue, result, **self.kwargs)
            #pass
            if status == None:
                continue
            elif status == False:
                new_doc = out
                self.inq.put(new_doc)
            elif status == True:
                self.outq.put(out)
        self._log("{} exit this threads".format(self.getName()))
