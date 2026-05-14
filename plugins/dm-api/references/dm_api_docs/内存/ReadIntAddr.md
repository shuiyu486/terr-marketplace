函数简介:

读取指定地址的整数数值，类型可以是8位，16位 32位 或者64位

函数原型:  
  
LONGLONG ReadIntAddr(hwnd,addr,type)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

type 整形数: 整数类型,取值如下

      0 : 32位

      1 : 16 位

      2 : 8位

      3 : 64位

      4 : 32位无符号

      5 : 16位无符号

      6 : 8位无符号

返回值:

长整形数:  
读取到的数值  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

value = dm.ReadIntAddr(hwnd,123456
,0)  
MessageBox  value

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。