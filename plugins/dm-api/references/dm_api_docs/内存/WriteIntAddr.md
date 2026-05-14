函数简介:

对指定地址写入整数数值，类型可以是8位，16位 32位 或者64位

函数原型:  
  
long WriteIntAddr(hwnd,addr,type,v)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

type 整形数: 整数类型,取值如下

      0 : 32位

      1 : 16 位

      2 : 8位

      3 : 64位

v 长整形数: 整形数值

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.WriteIntAddr(hwnd,123456,0,100)

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。