函数简介:

服务器压力太大,此函数不再支持。 请使用GetNetTimeByIp

函数原型:  
  
string GetNetTimeSafe()

参数定义:

返回值:  
  
字符串:  
时间格式. 和now返回一致. 比如"2001-11-01
23:14:08"

示例:

t = dm.GetNetTimeSafe()  
TracePrint "当前北京时间是:"&t  
  
注: 此接口不支持简单游平台.  
    如果程序无法访问时间服务器，那么空串.