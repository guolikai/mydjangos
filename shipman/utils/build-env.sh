#!/bin/bash
pip3 install -r /shipman-env/lib/python3.6/site-packages/shipman/requirements/requirements.txt
#pip3 install pymysql sqlalchemy tornado docker docker-py pycurl
pip3  uninstall pycurl -y
export PYCURL_SSL_LIBRARY=nss
easy_install pycurl
