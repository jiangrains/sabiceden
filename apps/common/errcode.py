# -*- coding: utf-8 -*-

#//-----------------//
#// 全局错误码定义//
#//-----------------//

#error code
#|第一段系统代码（0000开始，16进制）|第二段为子系统（0000开始，16进制）
#0x|0000|0000

#//-----------------//
#// 通用错误码定义//
#//-----------------//

#/** 格式错误. */
FORMAT_ILLEGAL = "FORMAT_ILLEGAL"
FORMAT_ILLEGAL_CODE = 0x00000001

#token错误，一般用于数据库中找不到对应的账户
TOKEN_ILLEGAL = "TOKEN_ILLEGAL"
TOKEN_ILLEGAL_CODE = 0x00000002

#token已过期，需要重新登陆
TOKEN_EXPIRE = "TOKEN_EXPIRE"
TOKEN_EXPIRE_CODE = 0x00000003




#//-----------------//
#// 员工系统错误码定义//
#//-----------------//
#/** 门店ID错误(选错门店或者搜索不到该门店). */
STOREID_INVALID = "STOREID_INVALID"
STOREID_INVALID_CODE = 0x00010002

