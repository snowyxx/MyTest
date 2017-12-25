#coding:utf-8
import io
import time
logfile = io.open('yantestlog.txt', 'a', encoding='utf-8')
logfile.seek(0)
logfile.truncate()
counter = 0
print 'writing log to file yantestlog.txt\nenter ctrl+c to stop.'
while True:
	counter += 1
	logfile.write(u'yanxx 接收数据包:215 错误 logcounter: {}\n'.format(counter))
	logfile.flush()
	time.sleep(10)

