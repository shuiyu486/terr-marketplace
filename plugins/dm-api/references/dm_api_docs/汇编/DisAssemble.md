函数简介:

把指定的机器码转换为汇编语言输出

函数原型:  
  
string DisAssemble(asm\_code,base\_addr, is\_64bit)

参数定义:  
  
asm\_code 字符串: 机器码，形式如 "aa bb cc"这样的16进制表示的字符串(空格无所谓)

base\_addr 长整形数: 指令所在的地址

is\_64bit  整形数: 
表示asm\_code表示的指令是32位还是64位. 32位表示为0,64位表示为1

返回值:

字符串:  
MASM汇编语言字符串.如果有多条指令，则每条指令以字符"|"连接.

示例:

dm\_ret = dm.DisAssemble("81 05 E0 5A
47 00 01 00 00 00",&H435fde,0)  
MessageBox dm\_ret