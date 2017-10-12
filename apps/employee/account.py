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
    creator = models.ForeignKey(Administrator) #创建此员工账号的管理员
    signin_date = models.DateTimeField(auto_now = True) #最后登录时间
    forbidden_date = models.DateTimeField(auto_now = True) #账号被置为禁止登陆的时间
    forbidden_reason = models.IntegerField() #账号被置为禁止登陆的原因
    forbidden_operator = models.ForeignKey(Administrator) #设置禁止登陆的管理员
    token = models.CharField(max_length = 256) #令牌,通过AID换算生成
    token_expire_date = models.DateTimeField(default = timezone.now) #令牌过期时间
    objects = AccountManager() #重写Account的管理器

    def __unicode__(self):
        return self.phone

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

    #返回登陆会话的token
    def signin(self):
        self.token = get_uuid()
        self.token_expire_date = timezone.now() + datetime.timedelta(days = self.TOKEN_EXPIRE_DAYS)
        self.save()
        return self.token        

    def exit(self):
        self.token = ""
        self.save()

    def checktoken(self):
        return 0x0 if timezone.now() < self.token_expire_date else 0x1

    def modifypsw(self, newpassword):
        self.password = newpassword
        self.token = ""
        self.save()           

    def resetpsw(self):
        self.password = self.phone[-6:]
        self.token = ""
        self.save()   