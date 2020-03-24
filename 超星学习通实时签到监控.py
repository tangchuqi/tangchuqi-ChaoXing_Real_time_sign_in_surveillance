"""
①Python环境
Python3.6及以上版本，需要配备的库requests，json,time
代码运行软件：Pycharm
②手动登录
手动登录地址：http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1
③Cookie获取
在签到过程中最基本的就是用户的Cookie，相当于用户的身份证，在最初写的Python版本中，我直接将我自己的Cookie作为参数保存在代码中，但是经过测试发现由于每个用户的Cookie不同所以后出现报错，所以辛苦小伙伴们手动获取个人Cookie，放入代码中，详细Cookie获取流程如下图所示
注：登录完成后右键审核元素，可以来到此页面
"""
import requests
import json
import time
import random
import unicodedata
import os

def Init():
	global headers,coursedatas,activeList,activates,need_monitoring,lower_time,upper_time,server_chan_sckey
	#读取配置文件config.ini中的Cookie
	try:
		with open('config.ini', 'rb') as f:
			headers=json.loads((f.read()).decode())
	except:
		print("请确保config.ini文件存在，且其中的格式正确，即将退出")
		os.system("pause")
		exit()
	coursedatas=[]
	activeList=[]
	activates=[]
	need_monitoring=[]
	server_chan_sckey='xxx'  # 申请地址http://sc.ftqq.com/3.version
	lower_time=5*60
	upper_time=8*60

def backclazzdata():
	global coursedatas
	url="http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
	res=requests.get(url,headers=headers)
	cdata=json.loads(res.text)
	if cdata['result']!=1:
		print("请确保config.ini中的Cookie正确，否则课程列表获取失败，即将退出")
		os.system("pause")
		exit()
	for item in cdata['channelList']:
		if "course" not in item['content']:
			continue
		pushdata=dict()
		pushdata['courseid']=item['content']['course']['data'][0]['id']
		pushdata['name']=item['content']['course']['data'][0]['name']
		pushdata['imageurl']=item['content']['course']['data'][0]['imageurl']
		pushdata['classid']=item['content']['id']
		coursedatas.append(pushdata)
	print("获取成功")
	# print(coursedatas)

def str_len(Str):
	Sum=0
	for ch in Str:
		if unicodedata.east_asian_width(ch)in('F','W','A'):
			Sum+=2
		else:
			Sum+=1
	return Sum

def printdata():
	global need_monitoring,lower_time,upper_time,max_len
	index=1
	for item in coursedatas:
		print("%2d.课程名称:"%index+item['name'])
		index+=1
	need_monitoring=list(map(int,input("选择需要监控的课程标号，空格隔开(回车默认全部):\n").split()))
	if not need_monitoring:
		need_monitoring=list(range(1,index))
	index=1
	max_len=0
	print("监控课程如下:")
	with open("log.txt","a+") as f:
		f.write("监控课程如下:")
	for item in coursedatas:
		if index in need_monitoring:
			with open("log.txt","a+") as f:
				f.write(item['name']+'\t')
			max_len=max(max_len,str_len(item['name']))
			print(item['name'],end='\t')
		index+=1
	with open("log.txt","a+") as f:
		f.write("\n")
	print("\n设定完成")
	try:
		lower_time,upper_time=map(lambda x:int(x)*60,int(input("输入每轮监控时间上下限(分钟)，空格隔开(回车5~8分钟一轮):\n")))
	except:
		pass
	print("监控时间设置完毕，每%d到%d分钟监控一轮"%(lower_time//60,upper_time//60))



def taskactivelist(courseName,courseId,classId):
	global activeList,uid
	UID_Index=headers["Cookie"].find('UID=')
	uid=headers["Cookie"][UID_Index+4:headers["Cookie"].find(';',UID_Index)]
	url="https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId="+str(courseId)+"&classId="+str(classId)+"&uid="+uid
	res=requests.get(url,headers=headers)
	data=json.loads(res.text)
	activeList=data['activeList']
	#print(activeList)
	for item in activeList:
		if "nameTwo" not in item:
			continue
		if item['activeType']==2 and item['status']==1:
			signurl=item['url']
			aid=getvar(signurl)
			if aid not in activates:
				sign(courseName,item,aid,uid)
				activates.append(aid)

def getvar(url):
	var1=url.split("&")
	for var in var1:
		var2=var.split("=")
		if var2[0]=="activePrimaryId":
			return var2[1]
	else:
		print("未找到aid，即将退出")
		os.system("pause")
		exit()


def sign(courseName,item,aid,UID):
	url="https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+aid+"&uid="+UID+"&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
	res=requests.get(url,headers=headers)
	if res.text=="您已签到过了":
		return
	print("\n【签到】课程:%s有待签到的活动 活动名称:%s 活动状态:%s 活动时间:%s"%(courseName,item['nameOne'],item['nameTwo'],item['nameFour']))
	msg=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"课程:"+courseName
	msg_title=time.strftime("%H点%M分",time.localtime())+courseName
	if res.text=="success":
		msg+="签到成功！"
		with open("log.txt","a+") as f:
			f.write(msg+"\n")
		print(msg)
		requests.get('https://sc.ftqq.com/{}.send'.format(server_chan_sckey),params={'text':msg_title+'签到成功！','desp':msg})
	else:
		msg+="签到失败，失败原因:"+res.text
		with open("log.txt","a+") as f:
			f.write(msg+"\n")
		print(msg)
		requests.get('https://sc.ftqq.com/{}.send'.format(server_chan_sckey),params={'text':msg_title+'签到失败','desp':msg})
	
def startsign():
	ind=1
	every_course_upper_time=upper_time/len(need_monitoring)
	every_course_lower_time=lower_time/len(need_monitoring)
	while True:
		print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"监控运行中，第"+str(ind)+"次检查开始:")
		index=1
		for coursedata in coursedatas:
			if index in need_monitoring:
				taskactivelist(coursedata['name'],coursedata['courseid'],coursedata['classid'])
				print("课程《"+coursedata['name']+"》"+" "*(max_len-str_len(coursedata['name']))+"检查完成",end=',')
				sleep_time=(every_course_upper_time-every_course_lower_time)*random.random()+every_course_lower_time
				print("休眠%d秒"%int(sleep_time))
				time.sleep(sleep_time)
			index+=1
		print("监控完成，第"+str(ind)+"次检查完成\n")
		with open("log.txt","a+") as f:
			f.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+" 第"+str(ind)+"次检查完成\n")
		ind+=1
if __name__=='__main__':
	Init()
	backclazzdata()
	printdata()
	startsign()