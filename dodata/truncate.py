#!/usr/bin/env python2.7
#the raw copy from web
#author@alingse
#2016.08.1

from __future__ import with_statement

import os, sys


def truncate_tail(file,number):
    count = 0
    with open(file,'r+b') as f:
        f.seek(0, os.SEEK_END)
        end = f.tell()
        while f.tell() > 0:
            f.seek(-1, os.SEEK_CUR)
            char = f.read(1)
            if char != '\n' and f.tell() == end:
                print "No change: file does not end with a newline"
                return 1
                #exit(1)
            if char == '\n':
                count += 1
            if count == number + 1:
                f.truncate()
                print "Removed " + str(number) + " lines from end of file"
                return 0
                #exit(0) 
            f.seek(-1, os.SEEK_CUR)
    if count < number + 1:
        print "No change: requested removal would leave empty file"
    return 3
    #exit(3)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print sys.argv[0] + ": Invalid number of arguments."
        print "Usage: " + sys.argv[0] + " linecount filename"
        print "to remove linecount lines from the end of the file"
        exit(2)
    number = int(sys.argv[1])
    file = sys.argv[2]
    truncate_tail(file,number)

