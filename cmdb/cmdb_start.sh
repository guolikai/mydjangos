#!/bin/bash
DevProject="cmdb"
DevopsEnv="/App/workspace/devops-env/"

ScriptDir=$(cd $(dirname $0); pwd)
ScriptFile=$(basename $0)

fDevopsEnv(){
#    pip3 install virtualenv
    virtualenv -p python3 ${DevopsEnv}/${DevProject}-env --no-site-packages
    source ${DevopsEnv}/${DevProject}-env/bin/activate
    pip3 install django pycurl  pymysql
    deactivate

}

fStart(){
    echo "source ${DevopsEnv}/${DevProject}-env/bin/activate"
    source ${DevopsEnv}/${DevProject}-env/bin/activate
    #nohup python3  /App/workspace/python-devops/dbcount/manage.py  runserver 0.0.0.0:8001 &
    echo "nohup python3  ${ScriptDir}/manage.py  runserver 0.0.0.0:8000 &"
    nohup python3  ${ScriptDir}/manage.py  runserver 0.0.0.0:8000 &
    deactivate
}

case "$1" in
    "init"     )  fDevopsEnv;;
    "start"    )  fStart;;
       *       )
    echo "${ScriptFile} init      ${DevProject} 项目初始化"
    echo "${ScriptFile} start     ${DevProject} 项目启动"
    ;;
