函数简介:

把汇编缓冲区的指令转换为机器码 并用16进制字符串的形式输出

函数原型:  
  
string Assemble(base\_addr,is\_64bit)

参数定义:

base\_addr 长整形数: 用AsmAdd添加到缓冲区的第一条指令所在的地址

is\_64bit  整形数:  
表示缓冲区的指令是32位还是64位. 32位表示为0,64位表示为1

返回值:

字符串:  
机器码，比如 "aa bb
cc"这样的形式

示例:

code = dm.Assemble(&H405940,1)  
MessageBox code