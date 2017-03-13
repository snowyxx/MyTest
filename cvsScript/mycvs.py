#encoding:utf-8

import os
import re
import sys
import pdb
import time
import datetime
import subprocess
import logging
import logging.handlers
from conf import data, MYPRODUCT, MYLANGUAGE, MYEDITOR, MYNAME

#TODO: cvs setup and login
#TODO: send notification by mail


#loging settings
format = '%(asctime)s %(levelname)s %(message)s'
logFileName = r'output.log'
formatter = logging.Formatter(format)
infoLogger = logging.getLogger("infoLog")
infoLogger.setLevel(logging.INFO)
infoHandler = logging.handlers.RotatingFileHandler(
    logFileName, 'a', 1024*1024, 1)
infoHandler.setLevel(logging.INFO)
infoHandler.setFormatter(formatter)
terminalHandler = logging.StreamHandler()
terminalHandler.setFormatter(formatter)
terminalHandler.setLevel(logging.INFO)
infoLogger.addHandler(infoHandler)
infoLogger.addHandler(terminalHandler)

FRESHFILECOUNT = 0
NEEDSPATHCOUNT = 0
TOCIFILES = []


def runcmd(cmd):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outdata, errdata = p.communicate()
    statusCode = p.wait()
    return(statusCode, outdata, errdata)


def string2timestamp(timestr, timefmt='%Y-%m-%d %H:%M:%S'):
    dt_obj = datetime.datetime.strptime(timestr, timefmt)
    return time.mktime(dt_obj.timetuple())


def getLastEnVer(cnlog, enlog):
    '''
    To get the English version which since lastest your No-English version's update.
    It means from which English version we should update you No-English
    '''
    lastPartten = r'(?is)revision (.*?)\r?\s*date: (.*?) \+'
    cnVers = re.findall(lastPartten, cnlog)
    enVers = re.findall(lastPartten, enlog)
    lastcnVer, lastcntime = cnVers[0]
    lastcnTS = string2timestamp(lastcntime)
    enVers_ST = [(x, string2timestamp(y)) for (x, y) in enVers]
    lastenVer = 'None'
    for x, y in enVers_ST:
        if y > lastcnTS:
            lastenVer = x
        if lastenVer and y < lastcnTS:
            lastenVer = x
            break
    return lastenVer


def doCVS(product):
    global FRESHFILECOUNT, NEEDSPATHCOUNT, TOCIFILES
    languageList = ['en', MYLANGUAGE]
    if os.path.exists('log.txt'):
        os.remove('log.txt')
    if os.path.exists('diff.txt'):
        os.remove('diff.txt')
    products = []
    if product.lower() == 'my':
        products = MYPRODUCT
    elif product.lower() == 'all':
        products = data.keys()
    else:
        products.append(product)
    for toCheckProduct in products:
        toCheckProduct = toCheckProduct.upper()
        infoLogger.info('{}\n[-] TO PROCESS product: {}'.format('='*20, toCheckProduct))
        flag = False
        files2Open = []
        files2Diff = {}
        if toCheckProduct not in data:
            infoLogger.info('[!] We do not support this product name: {}'.format(toCheckProduct))
            possibleNames = [n for n in data.keys() if toCheckProduct in n]
            infoLogger.info('[!] Do you mean: {}'.format(' or '.join(possibleNames)))
            usage()
            continue
        for f in data[toCheckProduct]:
            if f['language'] in languageList:
                statusCommand = 'cvs status {}'.format(f['path'])
                infoLogger.info('[-] TO RUN: {}'.format(statusCommand))
                statusCode, outdata, errdata = runcmd(statusCommand)
                if not os.path.exists(f['path']):
                    flag = True
                    FRESHFILECOUNT += 1
                    continue
                statusRex = r'Status:\s(.*?)\r?\n'
                try:
                    status = re.search(statusRex, outdata).group(1)
                except Exception:
                    infoLogger.info('[!] error of running command {}:\n{}\n{}'.format(statusCode, errdata, outdata))
                    continue
                infoLogger.info('-------- Status is : {}'.format(status))
                if 'Needs Patch' == status:
                    NEEDSPATHCOUNT += 1
                    flag = True
                    properEnLastVer = 0
                    workingVerRex = r'Working revision:\s*(\S*)?\s'
                    storeVerRex = r'Repository revision:\s*(\S*)?\s'
                    workingVer = re.search(workingVerRex, outdata).group(1)
                    storeVer = re.search(storeVerRex, outdata).group(1)
                    f['workingVer'] = workingVer
                    f['storeVer'] = storeVer
                    files2Diff[f['path']] = f
                    infoLogger.info('-------- new version is :{}\tYour version is:{}'.format(storeVer, workingVer))
                    infoLogger.info('-------- Last update information:\n{}'.format(outdata))
                    if f['language'] != 'en':
                        infoLogger.info('\n[!] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n[!] No-English file has been modified recently. \n[!] Look into diff.txt and log.txt to find out what is new. \n[!] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        enfile = {}
                        enpath = ''
                        for x in data[toCheckProduct]:
                            if x['category'] == f['category'] and x['language'] == 'en':
                                enfile = x
                                enpath = x['path']
                                break
                        thislogcmd = 'cvs log -r{}:{} {}'.format(workingVer, storeVer, f['path'])
                        enlogcmd = 'cvs log {}'.format(enpath)
                        infoLogger.info('[-] TO RUN {}'.format(thislogcmd))
                        statusCode, thislog, errdata = runcmd(thislogcmd)
                        infoLogger.info('[-] TO RUN {}'.format(enlogcmd))
                        statusCode, enlog, errdata = runcmd(enlogcmd)
                        properEnLastVer = getLastEnVer(thislog, enlog)
                        if properEnLastVer != 'None':
                            files2Open.append(f['path'])
                            infoLogger.info('-------- [!] You should update your file base on en version: {}'.format(properEnLastVer))
                        enfile['properEnLastVer'] = properEnLastVer
                        files2Diff[enpath] = enfile
                        infoLogger.info('[-] TO WRITE log.txt')
                        logFile = open('log.txt', 'a')
                        logFile.write(thislog)
                        logFile.write('\n'*2)
                        logFile.write(enlog)
                        logFile.write('\n'*4)
                        logFile.close()
                    else:
                        category = f['category']
                        files2Open += [x['path'] for x in data[toCheckProduct] if x['category'] == category and x['language'] == MYLANGUAGE]
        if flag:
            cvsDiff(files2Diff)
            files2Open = list(set(files2Open))
            TOCIFILES += files2Open
            checkOut(toCheckProduct, files2Open)


def cvsDiff(files):
    for f in files.values():
        properEnLastVer = f.get('properEnLastVer', 0)
        storeVer = f.get('storeVer', 0)
        workingVer = f.get('workingVer', 0)
        if properEnLastVer == 'None':
            infoLogger.info('[*] en file did not update since your language file last ci by other one.')
            continue
        elif properEnLastVer:
            if not workingVer:
                infoLogger.info('[*] en file did not update since your last co.')
                continue
            elif storeVer == properEnLastVer:
                continue
            else:
                workingVer = properEnLastVer
        diffFile = open('diff.txt', 'a')
        diffcmd = 'cvs diff -r{} -r{} {}'.format(storeVer, workingVer, f['path'])  # cvs diff return code is 256 :)
        infoLogger.info('[-] TO RUN {}'.format(diffcmd))
        statusCode, outdata, errdata = runcmd(diffcmd)
        infoLogger.info('[-] TO WRITE diff.txt')
        diffFile.write(outdata)
        diffFile.write('\n'*4)
        diffFile.close()


def checkOut(toCheckProduct, files2Open):
    rootpath = data[toCheckProduct][0]['path'].split('/')[0]
    coCmd = 'cvs co {}'.format(rootpath)
    infoLogger.info('[-] TO CHECK OUT: {}'.format(coCmd))
    statusCode, outdata, errdata = runcmd(coCmd)
    infoLogger.info(outdata)

    if len(files2Open) > 0:
        openFilesCmd = '{} {}'.format(MYEDITOR, ' '.join(files2Open))
        infoLogger.info('[-] TO OPEN the files: {}'.format(openFilesCmd))
        runcmd(openFilesCmd)


def openFile(filepath):
    startEditorCmd = '{} {}'.format(MYEDITOR, filepath)
    infoLogger.info('[-] TO OPEN file: {}'.format(startEditorCmd))
    try:
        statusCode, outdata, errdata = runcmd(startEditorCmd)
        if statusCode > 0:
            infoLogger.info('[!] Could not open file {}.'.format(filepath))
            infoLogger.info(statusCode, outdata, errdata)
    except Exception as e:
        infoLogger.info('[!] Could not open your eidtor to open file {}.'.format(filepath))
        infoLogger.info(e)


def usage():
    infoLogger.info('-'*50)
    infoLogger.info('Usage:')
    infoLogger.info('python mycvs.py <product name>')
    sortedProductNames = data.keys()
    sortedProductNames.sort()
    infoLogger.info('\nSupported product names:\n {}'.format('  '.join(sortedProductNames).lower()))
    infoLogger.info('\nNOTE: Supported special names:\n')
    infoLogger.info('\t- my : the product names defined in MYPRODUCT of conf.py')
    infoLogger.info('\t- all : all products. (DO NOT DO THIS... It will take long long time)')
    infoLogger.info('\nNOTE: Product name IS NOT case  sensitive')
    infoLogger.info('-'*50)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        strttime = time.time()
        product = sys.argv[1]
        doCVS(product)
        for f in ['diff.txt', 'log.txt']:
            try:
                if os.path.exists(f):
                    lastModifyTime = os.path.getmtime(f)
                    if lastModifyTime >= strttime:
                        openFile(f)
            except Exception, e:
                infoLogger.info('[!] Exception happended when to to open file: {}\n{}'.format(f, e))

        infoLogger.info('[*] If you can not view all printing of this script, please open output.log to get all lines.')
        infoLogger.info(' >>>>>>>>>>>>>>>>>>>>> Summary <<<<<<<<<<<<<<<<<<<')
        infoLogger.info('\t - New file count: {}'.format(FRESHFILECOUNT))
        infoLogger.info('\t - Updated file count: {}'.format(NEEDSPATHCOUNT))
        if len(TOCIFILES)>0:
            infoLogger.info('\t - Check in command you would to run: ')
            infoLogger.info('\t cvs ci -m"by {0}" {1}'.format(MYNAME, ' '.join(TOCIFILES)))
