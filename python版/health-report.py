# -*- coding:utf-8 -*-
from __future__ import print_function
import requests
import re
from bs4 import BeautifulSoup as bs
import os
import win32com.client as client
import ctypes, sys
def pzdata(text):
	soup = bs(text,'html.parser')
	mdata=[]
	a=soup.select('.th_right.required.validate.radio_list')
	for la in a:
		item =la.contents[-2].select('input')
		temp={}
		temp["OptionName"]=item[0]['value']
		temp["SelectId"]=item[0]['name']
		temp["TitleId"]=item[0].parent['data-tid']
		temp["OptionType"]='0'
		mdata.append(temp)
	return(str(mdata).replace("'",'"').replace(' ',''))

def find(item,text,num=0):
	a=re.findall(item,text)
	if a:
		if num:
			return a[num]
		else:
			return a[0]
	else:
		return ''
def handle_data(text):
	

	data={
		'StudentId':find(r'<input name="StudentId".*?value="(.*?)" />',text),
		'Name':find(r'<input name="Name".*?value="(.*?)" />',text),
		'SpecialtyName':find(r'name="SpecialtyName".*value="(.+?)" />',text),
		'ClassName':find(r'name="ClassName".*?value="(.*?)"',text),
		'MoveTel':find(r'name="MoveTel".*value="(\d+?)"',text),
		'Province':find(r'<option value="(\d{2}0000)" selected="selected">',text,num=0),
		'City':find(r'name="City".*?data-defaultValue="(\d+)"',text),
		'County':find(r'name="County".*?data-defaultValue="(\d+)"',text),
		'ComeWhere':find(r'name="ComeWhere".*maxlength="50" value="(.*?)"',text),
		'FaProvince':find(r'<option value="(\d{2}0000)" selected="selected">',text,num=1),
		'FaCity':find(r'name="FaCity".*?data-defaultValue="(\d+)"',text),
		'FaCounty':find(r'name="FaCounty".*?data-defaultValue="(\d+)"',text),
		'FaComeWhere':find(r'name="FaComeWhere".*maxlength="50" value="(.*?)"',text),
		'Other':'',
		'GetAreaUrl':find(r'id="GetAreaUrl".*?value="(.*?)"',text),
		'IdCard':find(r'id="IdCard".*?value="(.*?)"',text),
		'ProvinceName':find(r'id="ProvinceName.*value="(.*?)"',text),
		'CityName':find(r'id="CityName.*value="(.*?)"',text),
		'CountyName':find(r'id="CountyName.*value="(.*?)"',text),
		'FaProvinceName':find(r'FaProvinceName.*value="(.*?)"',text),
		'FaCityName':find(r'id="FaCityName.*value="(.*?)"',text),
		'FaCountyName':find(r'id="FaCountyName.*value="(.*?)"',text),
		'radioCount':find(r'id="radioCount.*value="(.*?)"',text),
		'checkboxCount':find(r'id="checkboxCount.*value="(.*?)"',text),
		'blackCount':find(r'id="blackCount.*value="(.*?)"',text),
		'PZData':pzdata(text),
		'ReSubmiteFlag':find(r'"ReSubmiteFlag.*value="(.*?)"',text),
	}
	soup = bs(text,'html.parser')
	data['Sex']=soup.select('input[id=Sex]')[0]['value']
	data['SpeType']=soup.select('input[id=SpeType]')[0]['value']
	data['CollegeNo']=soup.select('input[id=CollegeNo]')[0]['value']
	data['SpeGrade']=soup.select('input[id=SpeGrade]')[0]['value']
	data['radio_1']=soup.select('input[name=radio_1]')[-1]['value']
	data['radio_2']=soup.select('input[name=radio_2]')[-1]['value']
	data['radio_3']=soup.select('input[name=radio_3]')[-1]['value']
	data['radio_4']=soup.select('input[name=radio_4]')[-1]['value']
	
	return data
def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False
def report(user):
	session=requests.session()

	'''user={
	'stuId':'2011111123',
	'stuName':'丁一',
	'IdCard':'123123'
	}
	'''
	headers={
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	}
	###login
	print('logining')
	print(user)
	login_url='http://xgsys.swjtu.edu.cn/SPCPTest/Web/'
	r=session.get(login_url,headers=headers)

	headers={
		'Accept': '*/*',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'http://xgsys.swjtu.edu.cn',
	'Referer': 'http://xgsys.swjtu.edu.cn/spcptest/web',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',

	}
	#学生信息
	data={
		'stuId':user['stuId'],
	'stuName':user['stuName'],
	'stuIdCard':user['IdCard'],
	}
	check_url='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Account/CheckIdCardUser'
	r=session.post(check_url,headers=headers,data=data)
	#1：账号密码完全匹配  2：学号匹配  3：信息完全不匹配，其他错误
	code=r.text.replace('"','')
	if code=='1':
		print('登陆成功')
	elif code=='2':
		print('只有学号匹配,,请删除health.ini后重试或直接修改health.ini')
		os.system('pause')
		exit()
	elif code=='3':
		print('信息完全不匹配,请删除health.ini后重试或直接修改health.ini')
		os.system('pause')
		exit()
	else:
		print('未知错误，请自行填写')
		os.system('pause')
		exit()

	###login
	header = {
	    'Cache-Control': 'max-age=0',
		'Origin': 'http://xgsys.swjtu.edu.cn',
		'Upgrade-Insecure-Requests': '1',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Referer': 'http://xgsys.swjtu.edu.cn/spcptest/web',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
	     }
	data={
		'txtUid':user['stuId'],
	'txtPwd':user['stuName'],
	'txtIdCard':user['IdCard'],
	'codeInput':'',
	}
	login_url='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Account/IdCardLogin'
	r=session.post(login_url,headers=headers,data=data)
	###choose sys
	###report
	headers={
		'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Referer': 'http://xgsys.swjtu.edu.cn/SPCPTest/Web/Account/ChooseSys',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	}
	report_index_url='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Report/Index'
	r=session.get(report_index_url,headers=headers)
	#print(r.text)
	if '当前采集日期已登记'in r.text:
		print('当前采集日期已登记')
	else:
		headers={
		'Cache-Control': 'max-age=0',
		'Origin': 'http://xgsys.swjtu.edu.cn',
		'Upgrade-Insecure-Requests': '1',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Referer': 'http://xgsys.swjtu.edu.cn/SPCPTest/Web/Report/Index',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		}
		data=handle_data(r.text)
		#print(data)
		print('提交信息')
		for k in data:
			print(k,data[k])
		report_post_url='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Report/Index'
		r=session.post(report_post_url,headers=headers,data=data)
		if '提交成功' in r.text:
			print('提交成功')
		else:
			print(r.text)
			print('提交失败！！！！！！！！！！！！！！！！！！')

	os.system('pause')
	exit()
######################################################
if __name__=='__main__':
	try:
		with open('./health.ini',encoding='utf-8')as f:
			user=eval(f.read())

	except:
		if is_admin():
			# 将要运行的代码加到这里
			try:
				with open('./health.ini',encoding='utf-8')as f:
					user=eval(f.read())
			except:
				shell = client.Dispatch("WScript.Shell")
				print('第一次使用需要输入您的信息，信息保留在本地health.ini文件中')
				user={}
				user['stuId']= input('请输入学号：')
				user['stuName']=input('请输入姓名：')
				user['IdCard']=input('请输入身份证后6位：')
				with open('./health.ini','w+',encoding='utf-8')as f:
					f.write(str(user))
			
		else:
			if sys.version_info[0] == 3:
				ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
			else:#in python2.x
				ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

	report(user)