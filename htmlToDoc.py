#coding:utf-8
'''
Created on 2014年11月19日
python: 3 and pywin32
@author: yan
'''
import win32com.client
import xml.dom.minidom
import os
import shutil
import re
import sys
import time
from _operator import itemgetter
productDict={'op':r'op\helpIQ\help.xml',
    'ap':r'ap\AP_12_help\index.html',
    'ela':r'ela\v8-zh\index.html',
    'sdp_user':r'sdp\zh\userguide\index.html',
    'sdp_admin':r'sdp\zh\adminguide\index.html',
    'nfa':r'nfa\NetFlowAnalyzer_zh_95\index.html',
    'ada':r'ADAuditPlus\help\index.html',
    'adssp_user':r'adssp\user-guide\index.html',
    'adssp_admin':r'adssp\admin-guide\index.html',
    'adm':r'ADManager\help\index.html',
    'dc':r'DesktopCentral\DC_CN_90044\help\index.html',
    'de':r'DeviceExpert\5910\help_cn\index.html',
    'fwa':r'fwa\v4_cn\index.html',
    'opstor':r'opstor\opstor_help\index.html',
    'opu':r'OpUtils\help\index.html'}
def prepareHtml(fileList,product,path):
    pwd=os.getcwd()
    htmltemp=pwd+'\\temp_html'
    if os.path.exists(htmltemp):
        shutil.rmtree(htmltemp)
    shutil.copytree(path,htmltemp)
    
    pattern_RMLinksC=re.compile(r'(?i)<a(?![^>]*https?).*?>(.*?)</a>')
    pattern_RMxmlMarkC=re.compile(r'(?i)<\?xml.*?>')  #fix issue:Word 在处理 XML 文件 gantt_chart.html\n禁用 DTD
    pattern_joinAllLinesC=re.compile(r'\n')
    pattern_GoTopC=re.compile(r'(?i)<p[^>]*>\[?<a[^>]*>(问题列表|top|页首|问题|返回|问题)</a>\]?</p>')
    
    pattern_opImgC=re.compile(r'(?i)(<img.*?src=".*?)\?.*?(")')
    
    pattern_apmNavigatorC=re.compile(r'(?i)<table class="?(HDR|FTR)_TABLE(.|\n)*?</table>')
    pattern_apmFooterC=re.compile(r'(?i)<div class="footer".*?</div>')

    pattern_elaFooterC=re.compile(r'(?i)<div[^<]*<div[^<]*>copyright.*</div>')
    pattern_elaHomeC=re.compile(r'(?i)<td[^<]*<p.*?>.*».*?</p>\s*</td>')
    pattern_elaBlankC=re.compile(r'(?i)<tr>\s*<td[^>]*(bottom|top)">(&nbsp;|\s)*</td>')

    pattern_SDPFooterC=re.compile(r'(?i)<hr[^<]*<a.*copyright.*</html>')
    
    pattern_NFAFooterC=re.compile(r'(?i)(<hr>)?\s*<div[^<]*<div.*copyrigh.*(\.|Engine)(</div>)?\s*(</div>)?')
    pattern_NFAHeadC=re.compile(r'(?i)<div id="header"><table class="headtable">.*?</table></div>')
    
    pattern_adaFooterC=re.compile(r'(?i)<div[^<]*?>\s*<div[^<]*?(<a[^>]*>[^<]*</a>\s*)?版权所有.*?</div>.*?<div.*?</div></div>')
    pattern_adaGotoC=re.compile(r'(?i)<a[^>]*>(top|Questions)</a>')
    
    pattern_admFooterC=re.compile(r'(?i)<hr[^>]*>(\s*<p>)?\s*<font.*?</font>(\s*</p>)?')
    pattern_admHeadC=re.compile(r'(?i)<iframe.*?</iframe>')

    pattern_deHeaderC=re.compile(r'(?i)<p.*?>DeviceExpert主页.*在线演示.*?</p>')
    pattern_deFooterC=re.compile(r'(?i)<hr.*?><p.*?版权所有.*?</p>')
    
    pattern_fwaHeaderC=re.compile(r'(?i)<div\s+id="header".*?<?div>')
    pattern_fwaNaviC=re.compile(r'(?i)<table[^>]*navigator.*?</table>')
    pattern_fwaFooterC=re.compile(r'(?i)<hr>\s*<span.*?copy.*</span>')
    
    pattern_opstorFooterC=re.compile(r'(?i)<div[^<]*?>\s*<div[^<]*?copyright.*?</div>.*?<div.*?</div></div>')
    
    
    errordict={}
    for x in fileList:
        try:
            orgFilePath=htmltemp+'/'+x
            bakFilePath= orgFilePath+'~'
            shutil.move(orgFilePath,bakFilePath)
            enc='utf-8'
            try:
                srcFile=open(bakFilePath, mode='r',encoding=enc)
                fileContent=pattern_joinAllLinesC.sub('',srcFile.read())
            except UnicodeDecodeError:
                try:
                    enc='gbk'
                    srcFile=open(bakFilePath, mode='r',encoding=enc)
                    fileContent=pattern_joinAllLinesC.sub('',srcFile.read())
                except UnicodeDecodeError:
                    enc='iso-8859-1'
                    srcFile=open(bakFilePath, mode='r',encoding=enc)
                    fileContent=pattern_joinAllLinesC.sub('',srcFile.read())
            except:
                print('!!!!!!!!!!Error while read html file: '+x)
            
            fileContent=pattern_GoTopC.sub('',fileContent)
            
            if 'op'==product:
                fileContent=pattern_opImgC.sub(lambda m:m.group(1)+m.group(2),fileContent)
            elif 'ap'==product:
                fileContent=pattern_apmNavigatorC.sub('',fileContent)
                fileContent=pattern_apmFooterC.sub('',fileContent)
            elif 'ela'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_elaFooterC.sub('',fileContent)
                fileContent=pattern_elaHomeC.sub('',fileContent)
                fileContent=pattern_elaBlankC.sub('',fileContent)
            
            elif 'sdp_user'==product or 'sdp_admin'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_SDPFooterC.sub('</body></html>',fileContent)
                
            elif 'nfa'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_NFAFooterC.sub('',fileContent)
                fileContent=pattern_NFAHeadC.sub('',fileContent)

            elif 'ada'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_adaFooterC.sub('',fileContent)
                fileContent=pattern_adaGotoC.sub('',fileContent)

            elif 'adssp_user'==product or 'adssp_admin'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_adaFooterC.sub('',fileContent)
            
            elif 'adm'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_admFooterC.sub('',fileContent)
                fileContent=pattern_admHeadC.sub('',fileContent)
            
            elif 'dc'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_opstorFooterC.sub('',fileContent)
                fileContent=pattern_admHeadC.sub('',fileContent)
                pass
            
            elif 'de'==product:
                fileContent=pattern_deHeaderC.sub('',fileContent)
                fileContent=pattern_deFooterC.sub('',fileContent)
            
            elif 'fwa'==product:
                fileContent=pattern_fwaHeaderC.sub('',fileContent)
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_fwaFooterC.sub('',fileContent)
            
            elif 'opstor'==product:
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_opstorFooterC.sub('',fileContent)
            
            elif 'opu'==product:
                fileContent=pattern_admHeadC.sub('',fileContent)
                fileContent=pattern_fwaNaviC.sub('',fileContent)
                fileContent=pattern_opstorFooterC.sub('',fileContent)
            else:
                print("Product name is woring!!!!")
                sys.exit()
            
            fileContent=pattern_RMLinksC.sub(lambda m:m.group(1),fileContent)
            fileContent=pattern_RMxmlMarkC.sub('',fileContent)
            desFile=open(orgFilePath,'w',encoding=enc)
            desFile.write(fileContent)
            srcFile.close()
            desFile.close()
            print('----'+product+'------ prepare html Success with: '+x)
        except Exception as e:
            print('****'+product+'****** prepare html Error when handling: '+x)
            raise e
            errordict[x]=e
    return errordict
    
def getHtmlList(product,path):
    indexFilePathAP=path+'\\am_toc.html'
    indexFilePathELA=path+'\\script\\tree_nodes.js'
    indexFilePathSDP=path+'\\scripts\\tree_nodes.js'
    indexFilePathDE=path+'\\toc.html'
    indexFilePathOpStor=path+'\\opstor_toc.html'
    
    htmlPatternCAP=re.compile(r'(?i)href="(?P<toGet>.*?\.html)(?:"|#)')
    htmlPatternCELA=re.compile(r'(?i)["\']([^"\']*?\.html)["\']')
    
    commentPattenCAP=re.compile(r'<!--(.|\n)*?-->')
    commentPattenCELA=re.compile(r'\/\*(.|\n)*?\*\/')
    
    if 'op'==product:
        return getHtmlListForOPM(path)
    elif 'ap'==product:
        indexFilePath=indexFilePathAP
        contenC=htmlPatternCAP
        commentPattenC=commentPattenCAP
    elif 'ela'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'sdp_user'==product or 'sdp_admin'==product:
        indexFilePath=indexFilePathSDP
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'nfa'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'ada'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA

    elif 'adssp_user'==product or 'adssp_admin'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'adm'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    
    elif 'dc'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'de'==product:
        indexFilePath=indexFilePathDE
        contenC=htmlPatternCAP
        commentPattenC=commentPattenCAP
    elif 'fwa'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    elif 'opstor'==product:
        indexFilePath=indexFilePathOpStor
        contenC=htmlPatternCAP
        commentPattenC=commentPattenCAP
    elif 'opu'==product:
        indexFilePath=indexFilePathELA
        contenC=htmlPatternCELA
        commentPattenC=commentPattenCELA
    else:
        print("Product name is woring!!!!")
        sys.exit()
    try:
        indexFile=open(indexFilePath,encoding='utf-8')
        indexContent=commentPattenC.sub('',indexFile.read())
    except UnicodeDecodeError:
        indexFile=open(indexFilePath,encoding='gbk')
        indexContent=commentPattenC.sub('',indexFile.read())
    except:
        print('!!!!!!!Error while get file list.')
    htmlList=contenC.findall(indexContent)
    singleList=[]
    for x in htmlList:
        if x not in singleList:
            singleList.append(x)
    htmlListFinal=list(filter(lambda x:not x.startswith('http://www'),singleList))
    return htmlListFinal


def getHtmlListForOPM(path):
    #get the html file lisat that need covert to doc from OPM index file
    htmlList=[]
    fileList=[]
    DomTree=xml.dom.minidom.parse(path+'\\help.xml')
    collection=DomTree.documentElement

    pages=collection.getElementsByTagName('page')
    pageDict={}
    for page in pages:
        file_name=page.getElementsByTagName('file_name')[0].childNodes[0].data
        topic_id=page.getElementsByTagName('topic_id')[0].childNodes[0].data
        pageDict[topic_id]=file_name
    # print(pageDict)
    # print(len(pageDict))

    nodeList=[]
    orders=collection.getElementsByTagName('order')
    for order in orders:
        parent_id=order.getElementsByTagName('parent_id')[0].childNodes[0].data
        node_id=order.getElementsByTagName('node_id')[0].childNodes[0].data
        node_order=order.getElementsByTagName('node_order')[0].childNodes[0].data
        node_type=order.getElementsByTagName('node_type')[0].childNodes[0].data

        nodeList.append({'node_order':node_order,'node_id':node_id,'parent_id':parent_id,'node_type':node_type})

    node1=list(filter(lambda x:x['parent_id']=='0',nodeList))
    sortedNode1=sorted(node1,key=lambda x:int(x['node_order']))
    walkNode(sortedNode1,nodeList,htmlList)
    for x in htmlList:
        fileList.append(pageDict[x])
        # del pageDict[x]  #if you want to check which page is not included, use this
    # print(pageDict)  #if you want to check which page is not included, use this
    
    fileList.insert(0,'OpManager_User_Guide.html')  #add home page
    # print(len(fileList))
    return fileList

def walkNode(nodes,nodeList,htmlList):
    for n in nodes:
        if (n['node_type']=='F'):
            n_sub=list(filter(lambda x:x['parent_id']==n['node_id'],nodeList))
            sortedn_sub=sorted(n_sub,key=lambda x:int(x['node_order']))
            walkNode(sortedn_sub,nodeList,htmlList)
        else:
            htmlList.append(n['node_id'])


def htmlToDoc(fileList,product):
    pwd=os.getcwd()
    htmltemp=pwd+'\\temp_html'
    word = win32com.client.DispatchEx('Word.Application')
    # word.Visible=1
    finalDoc=word.Documents.Add()
    errordict={}
    allCount=len(fileList)
    count=0
    for x in fileList:
        count=count+1
        filePath=htmltemp+'\\'+x
        try:
            doc = word.Documents.Add(filePath)
            docFile=htmltemp+'\\'+x+'.docx'
            try:
                i=0
                s=len(doc.InlineShapes)
                while(i<s):
                    if doc.InlineShapes[i].Type==4: #4=word.WdInlineShapeType.wdInlineShapeLinkedPicture
                        doc.InlineShapes[i].LinkFormat.Update()
                        link=doc.InlineShapes[i].LinkFormat.SourceFullName
                        print(r' '*16+'going to handle picture: '+str(i)+"/"+str(s)+' -->'+link)
                        doc.InlineShapes[i].LinkFormat.SavePictureWithDocument=True
                    i=i+1
            except Exception as e:
                errordict[x]=e
                print(r' '*16+'Handle picture problem: '+e)
            doc.SaveAs(docFile, FileFormat=12)
            doc.Close()
            print('----'+product+'----- '+str(count)+'/'+str(allCount)+' convert doc Success with: '+x)
            finalDoc.Application.Selection.Range.InsertFile(docFile)
            finalDoc.Application.Selection.Range.InsertBreak(3) #3=word.WdBreakType.wdSectionBreakContinuous
            finalDoc.Application.Selection.EndKey(6,0)  #6=word.WdUnits.wdStory  0=word.WdMovementType.wdMove  
        except Exception as e:
            print('****'+product+'****** convert doc Error when handling: '+x)
            print(e)
            errordict[x]=e
    i=0
    while(i<len(finalDoc.Tables)):
        try:
            finalDoc.Tables[i].AutoFitBehavior(2) #2=Word.WdAutoFitBehavior.wdAutoFitWindow
            i=i+1
        except Exception as e:
            errordict[x]=e
            print(r' '*16+'Error when set autofix of table: '+e)
    try:
        finalDoc.ActiveWindow.View.Type=3  #3=Word.WdViewType.wdPrintView
        finalDoc.SaveAs(pwd+'\\'+product+'_help_'+time.strftime('%H%M%S',time.localtime(time.time()))+'.docx',FileFormat=12)
    except Exception as e:
        print(r' '*16+'Error when save final docx file: '+e)
        errordict[x]=e
    finally:
        finalDoc.Close()
        word.Quit()
    shutil.rmtree(htmltemp)
    print('!!!!!! DONE')
    return errordict

def doit(args):
    global productDict
    if len(args)<1:
        usage()
        sys.exit(0)
    product=args[0].lower()
    if len(args)>1:
        path=args[1]
    if product in productDict.keys():
        productDict={product:path}
    elif 'all'==product:
        pass
    else:
        print('!!!!!!!!!Product name is not supported.')
        usage()
        sys.exit(0)
    for (pro,pa) in productDict.items():
        path=pa[:pa.rindex('\\')]
        product=pro
        fileList=getHtmlList(product,path)
        dd=prepareHtml(fileList, product,path)
        d=htmlToDoc(fileList, product)
        if len(dd)>0:
            print("!!!!!!!!!!!!!!!!!!!!!!!Errors when preparing HTML file:")
        for (k,v) in dd.items():
            print(k+'-->'+str(v))
        if len(d)>0:
            print("!!!!!!!!!!!!!!!!!!!!!!!Errors when creating DOC file:")
        for (k,v) in d.items():
            print(k+'-->'+str(v))
def usage():
    mypath=sys.argv[0]
    myname=mypath[mypath.rindex('\\')+1:] if '\\' in mypath else mypath
    print('Usage:\n\npython '+myname+' <product name> <index file path>\n')
    print('For Example:')
    for (pro,path) in sorted(productDict.items(),key=itemgetter(0)):
        print('python '+myname+' '+pro+' '+path)
    print('python '+myname+' all ----This will cost long long time')
    print('\nRequest: python3; pywin32; Windows OS; Office Word')
if __name__ == '__main__':
    args=sys.argv[1:]
#     args=['ela', 'ela\\v8-zh\\index.html']
    doit(args)

