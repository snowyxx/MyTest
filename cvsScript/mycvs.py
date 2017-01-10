#encoding:utf-8

import os
import re
import sys
import pdb
import time
import subprocess
from conf import data, MYPRODUCT, MYLANGUAGE, MYEDITOR

#TODO: cvs setup and login
#TODO: send notification by mail


def runcmd(cmd):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outdata, errdata = p.communicate()
    statusCode = p.wait()
    return(statusCode, outdata, errdata)


def doCVS(product):
    languageList = ['en', MYLANGUAGE]
    if os.path.exists('diff.txt'):
        os.remove('diff.txt')
    if os.path.exists('log.txt'):
        os.remove('log.txt')

    products = []
    if product.lower() == 'my':
        products = MYPRODUCT
    elif product.lower() in ['all', 'me', 'zoho']:
        products = data.keys()
    else:
        products.append(product)
    for toCheckProduct in products:
        toCheckProduct = toCheckProduct.upper()
        print '{}\n[-] TO PROCESS product: {}'.format('='*20, toCheckProduct)
        flag = False
        files2Open = []
        if toCheckProduct not in data:
            print '[!] The product does not support: {}'.format(toCheckProduct)
            usage()
            continue
        files = data[toCheckProduct]
        for f in files:
            if f['brand'] != product.lower() and product.lower() in ['all', 'me', 'zoho']:
                continue
            if f['language'] in languageList:
                statusCommand = 'cvs status {}'.format(f['path'])
                print '[-] TO RUN: {}'.format(statusCommand)
                # if 'Apiclient_zh_CN' in f['path']:
                #     pdb.set_trace()
                statusCode, outdata, errdata = runcmd(statusCommand)
                if not os.path.exists(f['path']):
                    flag = True
                    continue
                statusRex = r'Status:\s(.*?)\r?\n'
                try:
                    status = re.search(statusRex, outdata).group(1)
                except Exception:
                    # print '[!] Could not pickup status information, check above command output please...'
                    continue
                print '-------- Status is : {}'.format(status)
                if 'Needs Patch' == status:
                    flag = True
                    workingVerRex = r'Working revision:\s*(\S*)?\s'
                    workingVer = re.search(workingVerRex, outdata).group(1)
                    storeVerRex = r'Repository revision:\s*(\S*)?\s'
                    storeVer = re.search(storeVerRex, outdata).group(1)
                    print '-------- new version is :{}\tcurrent version is:{}'.format(storeVer, workingVer)
                    print '-------- Last update information:\n{}'.format(outdata)
                    diffFile = open('diff.txt', 'a')
                    diffcmd = 'cvs diff -r{} -r{} {}'.format(storeVer, workingVer, f['path'])  # cvs diff return code is 256 :)
                    print '[-] TO RUN {}'.format(diffcmd)
                    statusCode, outdata, errdata = runcmd(diffcmd)
                    print '[-] TO WRITE diff.txt'
                    diffFile.write(outdata)
                    diffFile.close()
                    if f['language'] != 'en':
                        files2Open.append(f['path'])
                        print '[!] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n[!] No-English file has been modified recently. \n[!] Look into diff.txt and log.txt to find out what is new. \n[!] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                        logcmd = 'cvs log -r{}:{} {}'.format(workingVer, storeVer, f['path'])
                        print '[-] TO RUN {}'.format(logcmd)
                        statusCode, outdata, errdata = runcmd(logcmd)
                        print '[-] TO WRITE log.txt'
                        logFile = open('log.txt', 'a')
                        logFile.write(outdata)
                        logFile.close()
                    else:
                        category = f['category']
                        files2Open += [x['path'] for x in data[toCheckProduct] if x['category'] == category and x['language'] == MYLANGUAGE]
                else:
                    continue
        if flag:
            files2Open = list(set(files2Open))
            checkOut(toCheckProduct, files2Open)


def checkOut(toCheckProduct, files2Open):
    # pdb.set_trace()
    rootpath = data[toCheckProduct][0]['path'].split('/')[0]
    coCmd = 'cvs co {}'.format(rootpath)
    print '[-] TO CHECK OUT: {}'.format(coCmd)
    statusCode, outdata, errdata = runcmd(coCmd)
    print outdata

    if len(files2Open)>0:
        openFilesCmd = '{} {}'.format(MYEDITOR, ' '.join(files2Open))
        print '[-] TO OPEN the files: {}'.format(openFilesCmd)
        runcmd(openFilesCmd)


def openFile(filepath):
    startEditorCmd = '{} {}'.format(MYEDITOR, filepath)
    print '[-] TO OPEN file: {}'.format(startEditorCmd)
    try:
        statusCode, outdata, errdata = runcmd(startEditorCmd)
        if statusCode > 0:
            print '[!] Could not open file {}.'.format(filepath)
            print statusCode, outdata, errdata
    except Exception as e:
        print '[!] Could not open your eidtor to open file {}.'.format(filepath)
        print e


def usage():
    print '-'*50
    print 'Usage:'
    print 'python mycvs.py <product name>'
    sortedProductNames = data.keys()
    sortedProductNames.sort()
    print '\nSupported product names:\n {}'.format('  '.join(sortedProductNames).lower())
    print '\nNOTE: Supported special names:\n'
    print '\t- my : the product names defined in MYPRODUCT of conf.py'
    print '\t- me : all ManageEngine products'
    print '\t- zoho : all zoho.com products'
    print '\t- all : all products. (DO NOT DO THIS... It will take long long time)'
    print '\nNOTE: Product name IS NOT case  sensitive'
    print '-'*50


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        strttime = time.time()
        product = sys.argv[1]
        doCVS(product)
        try:
            diffFileLastModifyTime = os.path.getmtime('diff.txt')
            logFileLastModifyTime = os.path.getmtime('log.txt')
            if diffFileLastModifyTime > strttime:
                openFile('diff.txt')
            if logFileLastModifyTime > strttime:
                openFile('log.txt')
        except OSError, e:
            pass
