#!/usr/bin/env python

import os
import io
import re
import sys
import shutil
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding("utf-8")

class MyHTMLParser(HTMLParser):
    entitydefs = None

    def unescape(self, s):
        if '&' not in s:
            return s

        def replaceEntities(s):
            s = s.groups()[0]
            try:
                if s[0] == "#":
                    s = s[1:]
                    if s[0] in ['x', 'X']:
                        c = int(s[1:], 16)
                    else:
                        c = int(s)
                    return unichr(c)
            except ValueError:
                return '&#'+s+';'
            else:
                # Cannot use name2codepoint directly, because HTMLParser supports apos,
                # which is not part of HTML 4
                import htmlentitydefs
                if HTMLParser.entitydefs is None:
                    entitydefs = HTMLParser.entitydefs = {'apos': u"'"}
                    for k, v in htmlentitydefs.name2codepoint.iteritems():
                        entitydefs[k] = unichr(v)
                try:
                    return self.entitydefs[s]
                except KeyError:
                    return '&'+s+';'

        # return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", replaceEntities, s)
        return re.sub(r"&(#?[xX]?[0-9a-fA-F]+);", replaceEntities, s)

def main(dir):
    h = MyHTMLParser()

    getcharset_pattern = r'(?i)content=.*?charset=(.*?)["\']'
    for currentpath, folders, files in os.walk(dir):
        for f in files:
            if f.endswith('.html'):
                filename = os.path.join(currentpath, f)

                fr = open(filename, 'r')
                fc = fr.read()
                finds = re.findall(getcharset_pattern, fc)
                if len(finds)>0:
                    htmlCharset = finds[0]
                else:
                    htmlCharset =''
                if htmlCharset == 'gb2312':
                    fc = re.sub(
                        getcharset_pattern, 'content="text/html; charset=utf-8"', fc)
                    shutil.move(filename, filename+"~")
                    with io.open(filename, 'w', encoding='utf-8') as fw:
                        fw.write(fc.decode('gbk'))
                elif htmlCharset == 'utf-8':
                    pass
                elif htmlCharset == 'iso-8859-1':
                    fc = io.open(filename, 'r', encoding='iso-8859-1').read()
                    fc = re.sub(
                        getcharset_pattern, 'content="text/html; charset=utf-8"', fc)
                    shutil.move(filename, filename+"~")
                    with io.open(filename, 'w', encoding='utf-8') as fw:
                        fw.write(h.unescape(fc))

if __name__ == '__main__':
    basedir = '.'
    if len(sys.argv) > 1:
        basedir = os.path.realpath(sys.argv[1])
    main(basedir)


##########
#   Since I only want to convert Chinese but other specile character.
#   So I use MyHTMLParser class with overwrithe monthed unescape.
#   https://hg.python.org/cpython/file/2.7/Lib/HTMLParser.py
#   https://hg.python.org/cpython/file/2.7/Lib/htmlentitydefs.py
##########


        