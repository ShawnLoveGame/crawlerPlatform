#!/usr/bin/env python2.7
#coding=utf-8
#author@shibin
#2016.05.27

import sys
import json

def dec_json(jsondoc, head = None):
    dec_doc = {}
    for key in jsondoc:
        value = jsondoc[key]

        k_head = key
        if head != None:
            k_head = '{}.{}'.format(head, key)

        if type(value) == dict:
            dec_v = dec_json(value, head = k_head)
            dec_doc.update(dec_v)
        elif type(value) == list:
            for i in range(len(value)):
                sub_v = value[i]
                i_head = '{}.{}'.format(k_head, i)
                dec_v = dec_json(sub_v, head = i_head)
                dec_doc.update(dec_v)
        else:
            dec_doc[k_head] = value

    return dec_doc


if __name__ == '__main__':    
    fin = sys.stdin
    fout = sys.stdout
    if len(sys.argv) >= 2:
        fin = open(sys.argv[1],'r')
    if len(sys.argv) >= 3:
        fout = open(sys.argv[2],'w')

    for line in fin:
        jsondoc = json.loads(line)
        dec_doc = dec_json(jsondoc)
        fout.write(json.dumps(dec_doc,ensure_ascii=False).encode('utf-8'))
        fout.write('\n')