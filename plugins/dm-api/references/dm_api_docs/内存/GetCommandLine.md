函数简介:

获取指定窗口所在进程的启动命令行

函数原型:  
  
string GetCommandLine(hwnd)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

返回值:

字符串:  
读取到的启动命令行

示例:

command = dm.GetCommandLine(hwnd)  
MessageBox  command