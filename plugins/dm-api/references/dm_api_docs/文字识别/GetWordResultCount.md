函数简介:

在使用GetWords进行词组识别以后,可以用此接口进行识别词组数量的计算.

函数原型:  
  
long GetWordResultCount(str)

参数定义:  
  
str 字符串: GetWords接口调用以后的返回值

返回值:

整形数:  
返回词组数量

示例:

s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)  
count = dm.GetWordResultCount(s)  
MessageBox count