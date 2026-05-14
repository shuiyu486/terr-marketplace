函数简介:

根据指定的窗口句柄，来获取对应窗口句柄进程下的指定模块的大小

函数原型:  
  
long GetModuleSize(hwnd,module)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

module 字符串: 模块名

返回值:

整形数:  
模块的大小

示例:

module\_size = dm.GetModuleSize(hwnd,"gdi32.dll")  
MessageBox  module\_size

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。