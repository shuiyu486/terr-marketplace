函数简介:

获取指定窗口所在的线程ID.

函数原型:  
  
long GetWindowThreadId(hwnd)

参数定义:

hwnd 整形数: 窗口句柄

返回值:

整形数:  
返回整型表示的是线程ID

示例:

thread\_id = dm.GetWindowThreadId(hwnd)