#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

from Wolf.models import UserProfile
from Sansa import models
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email')

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        depth=2             #数据库外健
        fields = ('name', 'sn','server','networkdevice')

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        depth = 2
        #fields = ('os_type', 'sn','server')
        fields = ('asset','os_type','os_distribution','os_release')