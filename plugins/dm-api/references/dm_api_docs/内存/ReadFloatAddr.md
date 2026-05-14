函数简介:

读取指定地址的单精度浮点数

函数原型:  
  
float ReadFloatAddr(hwnd,addr)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

返回值:

单精度浮点数:  
读取到的数值  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

value =
dm.ReadFloatAddr(hwnd,123456)  
MessageBox  value

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。