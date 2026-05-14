函数简介:

读取指定地址的字符串，可以是GBK字符串或者是Unicode字符串.(必须事先知道内存区的字符串编码方式)

函数原型:  
  
string ReadStringAddr(hwnd,addr,type,len)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

type 整形数: 字符串类型,取值如下

      0 : GBK字符串

      1 : Unicode字符串

      2 : UTF8字符串

len 整形数: 需要读取的字节数目.如果为0，则自动判定字符串长度.

返回值:

字符串:  
读取到的字符串  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

value =
dm.ReadStringAddr(hwnd,123456 ,0,0)  
MessageBox  value

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。