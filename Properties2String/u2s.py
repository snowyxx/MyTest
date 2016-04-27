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
            s = s.replace(r'\\', r'\\\\')
            s = s.replace(r'\n', r'\\n')
            s = s.replace(r'\t', r'\\t')
            s = s.replace(r'\r', r'\\r')
            s = s.replace(r'\b', r'\\b')
            s = s.replace(r'\\\\\b', r'\\\\b')
            s = s.replace(r'\\\\\n', r'\\\\n')
            s = s.replace(r'\\\\\t', r'\\\\t')
            s = s.replace(r'\\\\\r', r'\\\\r')
            s = s.replace(r"\'", r"\\'")
            s = s.replace(r'\"', r'\\"')
            try:
                s = s.decode("unicode-escape")
            except Exception, e:
                if error == '':
                    error += str(e) + '\n' + self.view.substr(region)+r'\n'
                else:
                    error += self.view.substr(region)+r'\n'

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
            tmp = self.getTmpStr("@#$", s)
            s = s.replace("\\", tmp)
            try:
                s = s.encode("unicode-escape")
            except Exception, e:
                if error == '':
                    error += str(e) + '\n' + self.view.substr(region)+r'\n'
                else:
                    error += self.view.substr(region)+r'\n'
            finally:
                s = s.replace(tmp, "\\")
            self.view.replace(edit, region, s)
        if error != '':
            sublime.error_message(error)

    def getTmpStr(self, tmp, s):
        tmp = tmp + "1"
        if s.find(tmp) > -1:
            tmp = getTmpStr(tmp, s)
        else:
            pass
        return tmp
