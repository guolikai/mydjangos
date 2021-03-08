#!/bin/bash
AppName='AutoOps'
AppInstallBase='/opt/workspace'
AppInstallDir=${AppInstallBase}/${AppName}_env/bin
AppProg=${AppInstallBase}/${AppName}_env/bin/python3

ScriptDir=$(cd $(dirname $0); pwd)
ScriptFile=$(basename $0)


# 获取PID
fpid()
{
    #AppMasterPid=$(ps ax | grep "${AppInstallDir}" | grep -v "grep" | awk '{print $1}' 2> /dev/null)
    AppMasterPid=$(ps ax | grep "${AppInstallDir}" | grep -v "grep" | awk '{print $1}' 2> /dev/null)
}

# 查询状态
fstatus()
{
    fpid
    if [ ! -f "${AppProg}" ]; then
        echo "${AppName} 未安装"
    else
        echo "${AppName} 已安装"
        if [ -z "${AppMasterPid}" ]; then
            echo "${AppName} 未启动"
        else
            echo "${AppName} 正在运行"
        fi
    fi
}


fAppInstallBase(){
    #pip3 install virtualenv
    test -d ${AppInstallBase} || mkdir -p ${AppInstallBase}
    #virtualenv -p python3 ${AppInstallBase}/${AppName}_env --no-site-packages
    virtualenv -p python3 ${AppInstallBase}/${AppName}_env
    source ${AppInstallBase}/${AppName}_env/bin/activate
    pip3 uninstall pycurl
    export PYCURL_SSL_LIBRARY=openssl
    pip3 install pycurl django==2.0.5 pymysql djangorestframework uwsgi
    deactivate
}

fStart(){
    echo "source ${AppInstallBase}/${AppName}_env/bin/activate"
    source ${AppInstallBase}/${AppName}_env/bin/activate
    #echo "nohup python3  ${ScriptDir}/manage.py  runserver 0.0.0.0:80 &"
    #nohup python3  ${ScriptDir}/manage.py  runserver 0.0.0.0:80 &
    /opt/workspace/AutoOps_env/bin/uwsgi --ini /opt/devops/AutoOps/django_uwsgi.ini
    /opt/script/nginx_waf_install.sh reload
    deactivate
}


# 停止
fstop()
{
    fpid

    if [ -n "${AppMasterPid}" ]; then
        kill -9 ${AppMasterPid}  &>/dev/null && echo "停止 ${AppName}" || echo "${AppName} 停止失败"
    else
        echo "${AppName} 未启动"
    fi
}

# 终止进程
fkill()
{
    fpid
    if [ -n "${AppMasterPid}" ]; then
        echo "${AppMasterPid}" | xargs kill -9 &>/dev/null
        if [ $? -eq 0 ]; then
            echo "终止 ${AppName} 主进程"
        else
            echo "终止 ${AppName} 主进程失败"
        fi
    else
        echo "${AppName} 主进程未运行"
    fi
}

# 重启
frestart()
{
    fpid
    [ -n "${AppMasterPid}" ] && fstop && sleep 1
    fStart
}


case "$1" in
    "status"   ) fstatus;;
    "init"     ) fAppInstallBase;;
    "start"    ) fStart;;
    "stop"     ) fstop;;
    "status"   ) fstatus;;
    "restart"  ) frestart;;
    "kill"     ) fkill;;
       *       )
    echo "${ScriptFile} init      ${AppName} 项目初始化"
    echo "${ScriptFile} status    ${AppName} 项目状态"
    echo "${ScriptFile} start     ${AppName} 项目启动"
    echo "${ScriptFile} stop      ${AppName} 项目停止"
    echo "${ScriptFile} restart   ${AppName} 项目重启"
    echo "${ScriptFile} kill      ${AppName} 终止进程"
    ;;
esac
