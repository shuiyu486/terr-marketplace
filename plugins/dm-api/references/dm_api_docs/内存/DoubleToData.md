函数简介:

把双精度浮点数转换成二进制形式.

函数原型:  
  
string DoubleToData(value)

参数定义:  
  
value 双精度浮点数: 需要转化的双精度浮点数

返回值:

字符串:  
字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

示例:

double\_data =  dm.DoubleToData(1.24)  
dm\_ret = dm.FindData(hwnd,"00000000-7fffffff",double\_data)