函数简介:

对指定地址写入双精度浮点数

函数原型:  
  
long WriteDoubleAddr(hwnd,addr,v)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

v 双精度浮点数: 双精度浮点数

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.WriteDoubleAddr(hwnd,123456 ,2.34)

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。