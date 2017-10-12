# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from employee.account import Account
from common.http_response_customer import HttpResponseCustomer
from common.errcode import *

COOKIE_MAX_AGE = 1209600 #for 2 weeks

# Create your views here.
@csrf_exempt
def signin(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body) #if not json data ,it will raise a except.
            phone = json_data["phone"]
            password = json_data["password"]
            storeid = json_data["storeid"]
            logging.debug("phone:%s password:%s storeid:%s " % (phone, password, storeid))
        except :
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        if phone == "" or password == "" or storeid == "":
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        try:
            account = Account.objects.get(phone = phone)
        except:
            return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"token":""})
        else:
            if account.password != password:
                return HttpResponseCustomer(errCode = PASSWORD_INVALID_CODE, reason = [PASSWORD_INVALID], data = {"token":""})

            if account.storeid != storeid:
                return HttpResponseCustomer(errCode = STOREID_INVALID_CODE, reason = [STOREID_INVALID], data = {"token":""})

            if account.status != Account.ACCOUNT_ACTIVE:
                return HttpResponseCustomer(errCode = ACCOUNT_FORBIDDEN_CODE, reason = [ACCOUNT_FORBIDDEN], data = {"token":""})

        token = account.signin()
        response = HttpResponseCustomer(errCode = 0, reason = [], data = {"token":token})
        cookie_age = COOKIE_MAX_AGE
        response.set_cookie("_nji_tk_", token, max_age = cookie_age)
        return response
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})


@csrf_exempt
def exit(request):
    if request.method == "GET":
        phone = request.GET.get("phone", "")
        token = request.GET.get("token", "")

        if phone == "" or token == "":
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})
        
        try:
            cookie_token = request.COOKIES["_nji_tk_"]
        except KeyError:
            cookie_token = ""
        if token != cookie_token:
            return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})

        try:
            account = Account.objects.get(phone = phone)
        except :
            return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {})
        else:
            if account.token != token:
                return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})

            if account.checktoken() != 0:
                return HttpResponseCustomer(errCode = TOKEN_EXPIRE_CODE, reason = [TOKEN_EXPIRE], data = {"token":token})

            account.exit()
            response = HttpResponseCustomer(errCode = 0, reason = [], data = {})
            response.delete_cookie("_nji_tk_", path = "/")
            return response
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})


@csrf_exempt
def checktoken(request):
    try:
        json_data = json.loads(request.body) #if not json data ,it will raise a except.
        token = json_data["token"]
    except :
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

    try:
        cookie_token = request.COOKIES["_nji_tk_"]
    except KeyError:
        cookie_token = ""
    if token != cookie_token:
        return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})

    if request.method == "POST" and token != "":
        try:
            account = Account.objects.get(token = token)
        except :
            return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

    if account.checktoken() != 0:
        return HttpResponseCustomer(errCode = TOKEN_EXPIRE_CODE, reason = [TOKEN_EXPIRE], data = {"token":token})
    else:
        return HttpResponseCustomer(errCode = 0, reason = [], data = {"token":token})        


@csrf_exempt
def modifypsw(request):
    if request.method == "POST":
        try:
            token = request.GET.get("token", "")
            json_data = json.loads(request.body)
            phone = json_data["phone"]
            oldpassword = json_data["oldpassword"]
            password = json_data["password"]
        except :
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        if phone == "" or oldpassword == "" or password == "":
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"phone":phone, "oldpassword":oldpassword, "password":password})

        try:
            cookie_token = request.COOKIES["_nji_tk_"]
        except KeyError:
            cookie_token = ""
        if token != cookie_token:
            return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})            

        try:
            account = Account.objects.get(phone = phone)
        except :
            return HttpResponseCustomer(errCode = ACCOUNT_INVALID_CODE, reason = [ACCOUNT_INVALID], data = {"phone":phone})
        else:
            if account.password != oldpassword:
                return HttpResponseCustomer(errCode = PASSWORD_INVALID_CODE, reason = [PASSWORD_INVALID], data = {"token":""})

            if account.token != token:
                return HttpResponseCustomer(errCode = TOKEN_ILLEGAL_CODE, reason = [TOKEN_ILLEGAL], data = {})

            if account.checktoken() != 0:
                return HttpResponseCustomer(errCode = TOKEN_EXPIRE_CODE, reason = [TOKEN_EXPIRE], data = {"token":token})

            account.modifypsw(password)
            return HttpResponseCustomer(errCode = 0, reason = [], data = {})
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})
