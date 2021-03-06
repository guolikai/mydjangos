#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

import os,sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options, parse_command_line
define('port', default=8000, type=int, help="run on the port")
from shipman.url import urls

def main():
    PORT = 8000
    SETTINGS = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        login_url="/login",
        cookie_secret="235lksjfASKJFlks=jdfGLKS=JDFLKSsfjlk234dsjflksdjffj/=sf"
    )
    application = tornado.web.Application(
        handlers=urls,
        **SETTINGS
    )
    parse_command_line()
    print('serve listen port %s' % options.port)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
