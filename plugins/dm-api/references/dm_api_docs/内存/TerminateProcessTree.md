函数简介:

根据指定的PID，强制结束进程以及此进程创建的所有子进程.

函数原型:  
  
long TerminateProcessTree(pid)

参数定义:  
  
pid 整形数:进程ID.

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

hwnd = dm.GetMousePointWindow()  
pid = dm.GetWindowProcessId(hwnd)  
dm.TerminateProcessTree pid

注:另外DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。