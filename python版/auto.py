# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import win32com.client as client
import ctypes, sys
from time import sleep

if __name__=='__main__':
	def GetShortCut(shortcut):
		return shell.CreateShortCut(shortcut).Targetpath
		 
	def createShortCut(filename, lnkname):
	    """filename should be abspath, or there will be some strange errors"""
	    shortcut = shell.CreateShortCut(lnkname)
	    shortcut.TargetPath = filename
	    shortcut.save()
	 
	def CreateShortCut(filename, lnkname):
	    createShortCut(os.path.abspath(filename), lnkname)
	def is_admin():
		try:
			return ctypes.windll.shell32.IsUserAnAdmin()
		except:
			return False
	if is_admin():
		# 将要运行的代码加到这里
		shell = client.Dispatch("WScript.Shell")
		print('尝试添加自启动')
		CreateShortCut('health-report.exe', 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/health.lnk')
		print('已填加开机自启')
		sleep(3)

	else:
		if sys.version_info[0] == 3:
			ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
		else:#in python2.x
			ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)






