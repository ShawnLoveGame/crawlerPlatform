#!/usr/bin/env python2.7
#coding=utf-8
#the raw copy from web
#author@alingse
#2016.08.1

from __future__ import with_statement

import os, sys


def truncate_tail(file,number,size=1024):

    with open(file,'r+b') as f:
        #seek END
        f.seek(0, os.SEEK_END)
        end = f.tell()
        _end = end
        _number = number

        #only patch the last line
        last_patch = True
        while end >0 and number > 0:
            if end < size:
                size = end

            f.seek(-1*size, os.SEEK_CUR)
            #data block
            data = f.read(size)
            #seek back -- read把指针移回去了
            f.seek(-1*size, os.SEEK_CUR)
            lines = data.split('\n')
            

            #'wwww\nsfds\nss\nwww'
            #['wwww','sfds','ss','www']
            #通常lines最后一个半行应该算到上一次读的那一行里面,所以应该去掉
            #但是文件末尾这一个半行也算做一行,因此这里有一个patch
            if not last_patch:
                lines.pop()
            else:
                #文件末尾是完整行,会多出一个 [...,'']
                if data[-1] == '\n':
                    lines.pop()
                last_patch = False

            #lines
            count = len(lines)
            print(count)
            if count <= number:
                number = number - count
                end = end - size
            else:
                #pop number lines
                for i in range(number):
                    lines.pop()

                back_data = '\n'.join(lines)+'\n'
                back_size = len(back_data)

                #seek back
                f.seek(back_size, os.SEEK_CUR)
                end = end -size + back_size
                number = 0

        if end == 0 and number >= 0:
            print("No change: requested removal would leave empty file: {} bytes,{} lines".format(_end,_number - number))
            return 3
        if end >0 and number == 0:
            f.truncate()
            print("Removed {} lines && {} bytes from end of file".format(_number,_end - end))
            return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print sys.argv[0] + ": Invalid number of arguments."
        print "Usage: " + sys.argv[0] + " linecount filename"
        print "to remove linecount lines from the end of the file"
        exit(2)
    number = int(sys.argv[1])
    file = sys.argv[2]
    truncate_tail(file,number)

