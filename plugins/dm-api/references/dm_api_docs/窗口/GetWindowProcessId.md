函数简介:

获取指定窗口所在的进程ID.

函数原型:  
  
long GetWindowProcessId(hwnd)

参数定义:

hwnd 整形数: 窗口句柄

返回值:

整形数:  
返回整型表示的是进程ID

示例:

process\_id =
dm.GetWindowProcessId(hwnd)