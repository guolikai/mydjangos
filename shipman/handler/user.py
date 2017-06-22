#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikais

from shipman.handler.base import BaseHandler
from shipman.settings import COOKIE_NAME
from shipman.model.check import Check

class Login(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("user/login.html", login_strings=dict(username="Username", password="Password"))

    def post(self, *args, **kwargs):
        input_username = self.get_argument("username")
        input_password = self.get_argument("password")
        check_result = Check.login_check(input_username, input_password)
        #print("Account check_result:",check_result)
        if check_result == "Invalid username":
            self.render("user/login.html", login_strings=dict(username="Invalid username", password="Password"))
        elif check_result == "Incorrect password":
            self.render("user/login.html", login_strings=dict(username="Username", password="Incorrect password"))
        elif check_result == "Admin":
            self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)
            self.redirect("main")
        #elif check_result == "Common":
        #    self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)
        #    self.redirect("/consearch")
        else:
            self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)
            self.redirect("user/login.html")

class Logout(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie(COOKIE_NAME)
        self.write("<script language='javascript'>top.window.location.href='/';</script>")