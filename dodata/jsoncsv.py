#!/usr/bin/env python2.7
#coding=utf-8
#author@alingse
#2016.05.27

from __future__ import print_function
import json
import argparse
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
    '''
    json_obj = {}
    for key in exp_obj:
        value = exp_obj[key]
        keys = key.split('.')
        this = json_obj
        for ikey in keys:
            if ikey.isdigit():
                pass
    '''
    return exp_obj


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--expand',action='store_true',help='choose `expand` a json')
    parser.add_argument('-c','--contract',action='store_true',help='choose `expand` a json')
    parser.add_argument('--demo',action='store_true',help='show some test demo')
    parser.add_argument('-o','--output',help='file for output, default is stdout')
    parser.add_argument('input', nargs='?', help='input file, default is stdin')
    args = parser.parse_args()

    if args.demo:
        def demo(d,func,log=print):
            log('this obj :')
            log(d)
            log('apply `{}` will change to'.format(func.__name__))
            log(func(d))
        d1 = {'s':{'w':[1,2,3,{'t':5}]}}
        demo(d1,expand_json)
        d2 = [{'1':{'s':[1,2,{'t':[3,{'w':1}]},{'w':1}]}}]
        demo(d2,expand_json)

        exit()
    else:
        if args.output != None:
            fout = open(args.output,'w')
        else:
            fout = sys.stdout
        if args.input != None:
            fin = open(args.input,'r')
        else:
            fin = sys.stdin
        
        if args.expand == args.contract:
            print('can not choose two or choose none')
            exit()
        if args.expand:
            func = expand_json
        if args.contract:
            func = contract_json
        for line in fin:
            obj = json.loads(line)
            new = func(obj)
            out = json.dumps(new,ensure_ascii=False).encode('utf-8')
            fout.write(out)
            fout.write('\n')

        exit()