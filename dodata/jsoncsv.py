#!/usr/bin/env python2.7
#coding=utf-8
#author@shibin
#2016.05.27

import json
import sys


def expand_json(json_obj, head = None):
    exp_obj = {}
    
    if type(json_obj) == dict:
        for key in json_obj:
            if head == None:
                k_head = key
            else:
                k_head = '{}.{}'.format(head,key)

            k_obj = json_obj[key]
            k_exp_obj = expand_json(k_obj,head = k_head)
            exp_obj.update(k_exp_obj)
    elif type(json_obj) == list:
        for i in range(len(json_obj)):
            if head == None:
                i_head = str(i)
            else:
                i_head = '{}.{}'.format(head,i)

            i_obj = json_obj[i]
            i_exp_obj = expand_json(i_obj,head = i_head)
            exp_obj.update(i_exp_obj)
    else:

        if head == None:
            head = ''

        value = json_obj
        exp_obj[head] = value

    return exp_obj
   

def contract_json(exp_obj):
    json_obj = {}
    for key in exp_obj:
        value = exp_obj[key]
        keys = key.split('.')
        this = json_obj
        for ikey in keys:
            if ikey.isdigit():
                pass
    pass


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--test':
        t1 = {'s':{'w':[1,2,3,{'t':5}]}}
        print(t1)
        print(expand_json(t1))
        t2 = [{'1':{'s':[1,2,{'t':[3,{'w':1}]},{'w':1}]}}]
        print(t2)
        print(expand_json(t2))
        exit()
    fin = sys.stdin
    fout = sys.stdout
    if len(sys.argv) >= 2:
        fin = open(sys.argv[1],'r')
    if len(sys.argv) >= 3:
        fout = open(sys.argv[2],'w')

    for line in fin:
        json_obj = json.loads(line)
        exp_obj = expand_json(json_obj)
        fout.write(json.dumps(exp_obj,ensure_ascii=False).encode('utf-8'))
        fout.write('\n')



