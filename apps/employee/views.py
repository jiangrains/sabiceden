# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from common.http_response_customer import HttpResponseCustomer
from common.errcode import *

# Create your views here.
@csrf_exempt
def signin(request):

    logging.debug("test!!!!!!!!!!!!!!!")

    if request.method == "POST":
        try:
            json_data = json.loads(request.body) #if not json data ,it will raise a except.
            phone = json_data["phone"]
            password = json_data["password"]
            storeid = json_data["storeid"]
            logging.debug("phone:%s password:%s storeid:%s " % (phone, password, storeid))
        except :
            logging.debug("111111")
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        if phone == "" or password == "" or storeid == "":
            return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {})

        response = HttpResponseCustomer(errCode = 0, reason = [], data = {"token":"token-temp"})
        return response
    else:
        return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})

@csrf_exempt
def exit(request):
    return HttpResponseCustomer(errCode = FORMAT_ILLEGAL_CODE, reason = [FORMAT_ILLEGAL], data = {"token":""})        
