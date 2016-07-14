#! /usr/bin/env python
#coding:utf-8
import rapidjson
import sys

printTrue=True if sys.argv[1]=="T" else False
printFalse=True if sys.argv[1]=="F" else False

for line in sys.stdin:
    try:
        j=rapidjson.loads(line.strip())
        if type(j)==dict:
            if printTrue:print line.strip()#Ejson.dumps(j,ensure_asii=False).encode('utf-8')
        else:
            if printFalse:print line.strip()#json.dumps(j,ensure_asii=False).encode('utf-8')
    except:
        if printFalse:print line.strip()#json.dumps(j,ensure_asii=False).encode('utf-8')
        pass

    
