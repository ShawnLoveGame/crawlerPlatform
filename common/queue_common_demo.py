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

import sys
from random import random, randint


#1% error
def task(a, b):
    p = random()
    sleep_rand(0, p / 10)
    if p > 0.99:
        return False
    return a * b


def run(doc, **kwargs):
    a, b = doc
    result = task(a, b)
    #0 == False -- > True
    # ``if result == False:``
    if result is False:
        return False, None
    return True, result


def readline(line, inq=None, **kwargs):
    c = line
    a = c - 1
    b = c + 1
    inq.put((a, b))


def writeout(out, fout, inq=None):
    doc, result = out
    fout[0] += result
    return True


def main():
    #fin=open(fins,'r')
    N = 1000
    fin = iter(range(1, N + 1))
    fout = [0]

    reader = read_tool(fin, readline)
    writer = write_tool(fout, writeout)
    main_tool(reader, run, check, writer)
    #n(n+1)(2n+1)/6
    print(fout[0], N * (N + 1) * (2 * N + 1) / 6 - N)


if __name__ == '__main__':
    main()
