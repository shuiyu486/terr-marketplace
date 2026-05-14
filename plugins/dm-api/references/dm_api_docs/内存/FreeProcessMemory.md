函数简介:

释放指定进程的不常用内存.

函数原型:  
  
long FreeProcessMemory(hwnd)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

返回值:

整形数:  
  
0 : 失败  
1 : 成功

示例:

dm.FreeProcessMemory hwnd

注: 此函数的原理并不是真正的释放进程内存，而是把进程中不常用的内存交换到虚拟内存中(硬盘里). 这样可以空余出系统ram.此函数会加大系统内存和硬盘之间的数据交换频率，不能频繁调用。
一般用法是程序长时间运行一段时间调用一次.