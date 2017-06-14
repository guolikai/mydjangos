#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

import django
import redis

def redis_conn(django_settings):
    #print(django_settings.REDIS_CONN)
    pool = redis.ConnectionPool(host=django_settings.REDIS_CONN['HOST'], port=django_settings.REDIS_CONN['PORT'])
    r = redis.Redis(connection_pool=pool)
    return  r