函数简介:

获取指定窗口所在的进程的exe文件全路径.

函数原型:  
  
string GetWindowProcessPath(hwnd)

参数定义:

hwnd 整形数: 窗口句柄

返回值:

字符串:  
返回字符串表示的是exe全路径名

示例:

process\_path =
dm.GetWindowProcessPath(hwnd)