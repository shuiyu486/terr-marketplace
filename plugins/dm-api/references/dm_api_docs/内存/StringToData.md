函数简介:

把字符串转换成二进制形式.

函数原型:  
  
string StringToData(value,type)

参数定义:  
  
value字符串: 需要转化的字符串  
type  整形数: 取值如下:  
           
0: 返回Ascii表达的字符串  
           
1: 返回Unicode表达的字符串  
           
2: 返回UTF8表达的字符串

返回值:

字符串:  
字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

示例:

string\_data =  dm.StringToData("12345678",1)  
dm\_ret = dm.FindData(hwnd,"00000000-7fffffff",string\_data)