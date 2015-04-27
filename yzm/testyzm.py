#coding=utf-8
from os import listdir

import yzm

from getimg import get_imgdata
from doimg import dealimg2
from makeyzm import showimg
from yzm import imgdata2img,img2imgdata,yzmimgdata,yzm,yzmimage

def main():
    """
    imgdata=get_imgdata()
    im=imgdata2img(imgdata)
    nim=dealimg2(im)
    testimgfname="test.jpg"
    nim.save(testimgfname)
    showimg(testimgfname).start()
    print ''.join(yzm(testimgfname))
    """

    test_dir="./test_data/"

    testfile_list = listdir('test_data')
    for filenamei in testfile_list:
        fname=test_dir+filenamei
        showimg(fname).start()
        imgdata=open(fname,'r').read()
        im=imgdata2img(imgdata)
        nim=dealimg2(im)
        result=yzmimage(nim)
        #nimgdata=img2imgdata(nim)
        #result=yzmimgdata(nimgdata)
        #result=yzm(fname)
        print ''.join(result)
        raw_input()


if __name__ == '__main__':
    main()

