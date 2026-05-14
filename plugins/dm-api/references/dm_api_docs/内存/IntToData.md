函数简介:

把整数转换成二进制形式.

函数原型:  
  
string IntToData(value,type)

参数定义:  
  
value 长整形数: 需要转化的整型数  
type  整形数: 取值如下:  
           
0: 4字节整形数 (一般都选这个)  
           
1: 2字节整形数  
           
2: 1字节整形数  
           
3: 8字节整形数

返回值:

字符串:  
字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

示例:

int\_data =  dm.IntToData(&H12345678,0)  
dm\_ret = dm.FindData(hwnd,"00000000-7fffffff",int\_data)