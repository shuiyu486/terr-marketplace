函数简介:

释放用VirtualAllocEx分配的内存.

函数原型:  
  
long VirtualFreeEx(hwnd,addr)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数:
VirtualAllocEx返回的地址

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

addr =
dm.VirtualAllocEx(hwnd,0,50,0)  
dm.WriteString hwnd,cstr(hex(addr)),0,"哈哈"  
dm.VirtualFreeEx hwnd,addr  
  
注:如果正常方式无法分配内存,可以尝试配合DmGuard中的memory护盾,突破部分窗口内存保护。  
用此函数分配的内存，必须用VirtualFreeEx来释放,以免目标进程内存泄漏.