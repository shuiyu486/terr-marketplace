函数简介:

对指定地址写入字符串，可以是Ascii字符串或者是Unicode字符串

函数原型:  
  
long WriteStringAddr(hwnd,addr,type,v)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

type 整形数: 字符串类型,取值如下

      0 : Ascii字符串

      1 : Unicode字符串

      2 : UTF8字符串

v 字符串: 字符串

返回值:

整形数:  
0: 失败

1: 成功

示例:

dm\_ret =
dm.WriteStringAddr(hwnd,123456 ,0,"我是来测试的")

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。