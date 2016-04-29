# encoding:utf-8

import sublime
import sublime_plugin


class UnicodeToString(sublime_plugin.TextCommand):

    def run(self, edit):
        error = ''
        if len(self.view.sel()) == 1 and self.view.sel()[0].empty():
            # nothing selected, then convert the whole document
            region = sublime.Region(0, self.view.size())
            dataRegion = self.view.lines(region)
        else:
            dataRegion = self.view.sel()
        for region in reversed(dataRegion):
            s = self.view.substr(region)
            line_continuation_character = False
            if s.endswith('\\'):
                line_continuation_character = True
                s = s[:-1]
            s = s.replace(r'\\', r'\\\\')
            s = s.replace(r'\a', r'\\a')
            s = s.replace(r'\b', r'\\b')
            s = s.replace(r'\f', r'\\f')
            s = s.replace(r'\n', r'\\n')
            s = s.replace(r'\r', r'\\r')
            s = s.replace(r'\t', r'\\t')
            s = s.replace(r'\v', r'\\v')
            s = s.replace(r'\o', r'\\o')
            s = s.replace(r'\x', r'\\x')
            s = s.replace(r'\\\\\a', r'\\\\a')
            s = s.replace(r'\\\\\b', r'\\\\b')
            s = s.replace(r'\\\\\f', r'\\\\f')
            s = s.replace(r'\\\\\n', r'\\\\n')
            s = s.replace(r'\\\\\r', r'\\\\r')
            s = s.replace(r'\\\\\t', r'\\\\t')
            s = s.replace(r'\\\\\v', r'\\\\v')
            s = s.replace(r'\\\\\o', r'\\\\o')
            s = s.replace(r'\\\\\x', r'\\\\x')
            s = s.replace(r"\'", r"\\'")
            s = s.replace(r'\"', r'\\"')
            s = s.replace(r'\u0020', r'BLANK!@#SPACE')
            try:
                s = s.decode("unicode-escape")
            except Exception, e:
                error += str(e) + '--' + self.view.substr(region)+'\n'
            if line_continuation_character:
                s += '\\'
            s = s.replace(r'BLANK!@#SPACE',r'\u0020')    
                
            self.view.replace(edit, region, s)
        if error != '':
            sublime.error_message(error)


class StringToUnicode(sublime_plugin.TextCommand):

    def run(self, edit):
        error = ''
        if len(self.view.sel()) == 1 and self.view.sel()[0].empty():
            # nothing selected, then convert the whole document
            region = sublime.Region(0, self.view.size())
            dataRegion = self.view.lines(region)
        else:
            dataRegion = self.view.sel()
        for region in reversed(dataRegion):
            s = self.view.substr(region)
            sl = []
            try:
                for ss in s:
                    if ord(ss) > 127:
                        ss = ss.encode("unicode-escape")
                    sl.append(ss)
                s = ''.join(sl)
            except Exception, e:
                error += str(e) + '--' + self.view.substr(region)+r'\n'
            self.view.replace(edit, region, s)
        if error != '':
            sublime.error_message(error)
