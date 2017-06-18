#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

from shipman.handler.user import Login, \
                          Logout
from shipman.handler.node import Main, \
                          NodeManage, \
                          Top, \
                          LeftGroup, \
                          GroupList, \
                          RightNode, \
                          ConCreate, \
                          ConAction, \
                          ConStart, \
                          ConStop, \
                          ConDestroy, \
                          ConRestart, \
                          ConManage, \
                          ConModify,\
                          NodeAdd,\
                          NodeModify,\
                          NodeDelete, \
                          Group

urls = [
    (r"/",           Login),
    (r"/login",      Login),
    (r"/logout",     Logout),
    (r"/main",       Main),
    (r"/base",       Top),
    (r"/leftgroup",  LeftGroup),
    (r"/grouplist",  GroupList),
    (r"/nodemanage", NodeManage),
    (r"/nodeadd",    NodeAdd),
    (r"/nodemodify", NodeModify),
    (r"/nodedelete/$", NodeDelete),
    (r"/node",        RightNode),
    (r"/concreate",   ConCreate),
    (r"/conaction",   ConAction),
    (r"/constart",    ConStart),
    (r"/constop",     ConStop),
    (r"/conrestart",  ConRestart),
    (r"/condestroy",  ConDestroy),
    (r"/conmanage",   ConManage),
    (r"/conmodify",   ConModify),
    (r"/group",       Group),
]