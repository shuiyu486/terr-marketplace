函数简介:

对插件部分接口的返回值进行解析,并返回ret中的坐标个数

函数原型:  
  
long GetResultCount(ret)

参数定义:  
  
ret 字符串: 部分接口的返回串

返回值:

整形数:  
返回ret中的坐标个数

示例:

s =
dm.FindColorEx(0,0,2000,2000,"123456-000000|abcdef-202020",1.0,0)  
count = dm.GetResultCount(s)  
MessageBox count