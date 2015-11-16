#!/usr/bin/evn python
# coding=utf-8

import os
import commands
import sys
import shutil

def getFiles(path):
    files = []
    for (p, d, f) in os.walk(path):
        for ff in f:
            if ff.split('.')[-1] == 'html':
                fp = os.path.join(p, ff)
                files.append(fp)
    return files


def stripM(files):
    for f in files:
        cmd = 'cat '+f+' | col -b'
        o = commands.getstatusoutput(cmd)
        if o[0] > 0:
            print '!!!!!!!!!!Error with '+f+' '+str(o[0])
        else:
            with open('new/'+f, 'w') as df:
                df.write(o[1])
            print 'Done with '+f


def main(path):
    if os.path.exists('new'):
        shutil.rmtree('new')
    shutil.copytree(path,'new/'+path)
    htmlFiles = getFiles(path)
    stripM(htmlFiles)


def usage():
    print '''
        Usage:
            python stripM.py path
            for example: python stripM.py html
    '''
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main(sys.argv[1])
