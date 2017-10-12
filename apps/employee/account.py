# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import django.utils.timezone as timezone
import datetime

from common.utils import get_uuid

class AccountManager(models.Manager):

    def add_account(self, phone, password):
        account = self.model(phone = email, password = password) #创建account实例
        account.save() #将实例写入数据库
        #TODO create user
        return account.phone


# Create your models here.
class Account(models.Model):
    ACCOUNT_ACTIVE = 0
    ACCOUNT_LOCKED = 1

    TOKEN_EXPIRE_DAYS = (2*7) #2 weeks
    
    #user = models.OneToOneField(User)
    phone = models.CharField(max_length = 32) #账户手机号
    password = models.CharField(max_length = 256)
    status = models.IntegerField(default = ACCOUNT_ACTIVE) #账号状态，0：正常，1：禁止登陆
    signup_date = models.DateTimeField(auto_now_add = True) #账号添加时间
    signin_date = models.DateTimeField(auto_now = True) #最后登录时间
    code = models.CharField(max_length = 256) #激活码
    code_expire_date = models.DateTimeField(default = timezone.now) #激活码过期时间
    token = models.CharField(max_length = 256) #令牌,通过AID换算生成
    token_expire_date = models.DateTimeField(default = timezone.now) #令牌过期时间
    objects = AccountManager() #重写Account的管理器

    def __unicode__(self):
        return self.username
