#!/usr/bin/env python3
# _*_ coding:utf8 _*_
import subprocess
class LinuxOSCommand(object):
    def __init__(self):
        pass
    def LinuxOsCommand(self,command):
        result=[]
        cmd_res = subprocess.getstatusoutput(command)    #python3
#        print(cmd_res)    #返回的结果是一个元组
        if cmd_res[0]==0:
            for item in cmd_res[1].split("\n"):
                result.append(item)
            return result
			

AppDir='/root/yanxiu-qiniu-convert'
#YouthComm="ls -l %s | grep -v 总用量 |awk '{print $6}' | uniq | sort|head -1" % AppDir
YouthComm="ls -l %s | grep -v 总用量 |awk '{print $6}' | awk -F'月' '{print $1}' | uniq | sort" % AppDir
LinuxOSCommand=LinuxOSCommand()
#Youth=LinuxOSCommand.LinuxOsCommand(YouthComm)[0]
Youth=LinuxOSCommand.LinuxOsCommand(YouthComm)
print(Youth)
#ll | awk '{if($6~'11' && $7=='16' && $8~'04')print $9}'
DayComm="ls -l %s | grep -v 总用量 |awk '{if($6~\"%s\") print $7}'|uniq|sort"  % (AppDir,Youth)
#print(LinuxOSCommand.LinuxOsCommand(DayComm))
MaxDayList=LinuxOSCommand.LinuxOsCommand(DayComm)
MaxDay=list(map(int,MaxDayList))
print(max(MaxDay))

TimeComm="ls -l %s | grep -v 总用量 |awk '{if($6~\"%s\" && $7==\"%s\") print $8}'|uniq|sort"  % (AppDir,Youth,max(MaxDay))
TimeList=LinuxOSCommand.LinuxOsCommand(TimeComm)
Len=len(TimeList)
print(TimeList)
LastTime=TimeList[Len -2]

FileNameComm="ls -l %s | grep -v 总用量 |awk '{if($6~\"%s\" && $7==\"%s\" && $8==\"%s\") print $9}'|uniq|sort"  % (AppDir,Youth,max(MaxDay),LastTime)
FileNameList=LinuxOSCommand.LinuxOsCommand(FileNameComm)
#print(%s%s) % (AppDir,FileNameList[0])
FileName="%s/%s" % (AppDir,FileNameList[0])
print(FileName)

