#!/bin/bash
source /root/workspace/python3-env/bin/activate
nohup python3  /root/workspace/python-dev/dbcount/manage.py  runserver 0.0.0.0:8001 &
deactivate
