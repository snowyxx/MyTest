#!/usr/bin/env python
import os
import sys
import io
import subprocess

excludedFileType = ("mov", "mp4", "avi", "wmv", "lxe", "mpg",
                    "MOV", "ttc", "MP4", "AVI", "WMV", "LXE", "MPG", "TTC")

excludeFile = 'excludedFiles.txt'


def main(source, destination):
    check = checkMount(source)
    if not check:
        return
    updateExcludeFile(source)
    runRsync(source, destination)


def checkMount(source):
    if os.path.exists(source):
        return True
    else:
        print '!'*8+'Source does not exists!!! Mount it first!!!'
        print '!'*8+'e.g. mkdir /volumes/source;mount_smbfs //username@removehost/sharefolder /volumes/source'
        return False


def updateExcludeFile(source):
    toWrite = ".svn"
    for (path, ds, fs) in os.walk(source):
        if path.startswith('.'):
            continue
        for f in fs:
            if f.endswith(excludedFileType):
                toWrite += "\n"
                toWrite += f

    with io.open(excludeFile, 'wb') as wf:
        wf.write(toWrite)

    print '-'*8+'File to exclude: ' + toWrite


def runRsync(source, destination):
    command = 'rsync -av --progress --exclude-from=' + \
        excludeFile+' '+source+' '+destination
    # command = 'python -u test.py'
    print command
    status, output = runCMDBySubProcess(command)
    # rsync -av --progress --exclude-from=e.txt /Volumes/96d/test/ test/


def runCMDBySubProcess(cmd):
    p = subprocess.Popen(
        cmd, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    # http://stackoverflow.com/questions/2804543/read-subprocess-stdout-line-by-line
    for line in iter(p.stdout.readline, ''):
        print line,

    output, error = p.communicate()
    p_status = p.wait()
    # print p_status
    return (p_status, output)


if __name__ == '__main__':
    source = '/Volumes/96d/document/'
    destination = 'document/'
    if len(sys.argv) > 2:
        source = sys.argv[1]
        destination = sys.argv[2]
    main(source, destination)
