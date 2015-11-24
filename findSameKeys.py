#!/usr/bin/env python
'''
This script to find same key in diff file and other file(zh_CN)
'''

import re
import sys


def findSame(currentFile):
    diffLines = open(diffFile, 'r').readlines()
    newoldlines = filter(lambda x: re.search(r'^[<>].*=.*', x), diffLines)
    newlines = [x[2:].rstrip() for x in newoldlines if x.startswith('<')]
    newlines = list(set(newlines))
    oldlines = [x[2:].rstrip() for x in newoldlines if x.startswith('>')]
    samelines = []
    realNews = []
    print '-'*8+' new lines '+'-'*8
    for line in newlines:
        if line.startswith('#'):
            continue
        if line not in oldlines:
            print line
            realNews.append(line)
        else:
            samelines.append(line)

    print '-'*8+' same with old lines '+'-'*8
    for sl in samelines:
        print sl

    print '*'*8+' old line shoulbe remove '+'*'*8
    for ol in oldlines:
        if ol not in newlines:
            print ol

    return realNews


def findExist(realNews, otherFile):
    fileLines = open(otherFile, 'r').readlines()
    otherLines = filter(lambda x: re.search(r'^[^#].*=.*', x), fileLines)

    otherKeys = map(lambda x: x.split('=', 1)[0], otherLines)

    ns = [nl for nl in realNews if nl.split('=', 1)[0] not in otherKeys]

    print '*'*8+' new lines are not existing '+'*'*8
    for n in ns:
        print n

if __name__ == '__main__':
    diffFile = 'diff.txt'
    otherFile = 'EnglishToNative_zh_CN.properties'
    if len(sys.argv) == 3:
        diffFile = sys.argv[1]
        otherFile = sys.argv[2]
    realNews = findSame(diffFile)
    findExist(realNews, otherFile)
