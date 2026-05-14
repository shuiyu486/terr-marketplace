函数简介:

在指定的窗口所在进程分配一段内存.

函数原型:  
  
LONGLONG VirtualAllocEx(hwnd,addr,size,type)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr 长整形数: 预期的分配地址。 如果是0表示自动分配，否则就尝试在此地址上分配内存.

size **整形数**: 需要分配的内存大小.

type **整形数**: 需要分配的内存类型，取值如下:  
            
0 : 可读可写可执行  
            
1 : 可读可执行，不可写  
            
2 : 可读可写,不可执行

返回值:

长整形数:  
分配的内存地址，如果是0表示分配失败.

示例:

addr =
dm.VirtualAllocEx(hwnd,0,50,0)  
dm.WriteString hwnd,cstr(hex(addr)),0,"哈哈"  
dm.VirtualFreeEx hwnd,addr  
  
注:如果正常方式无法分配内存,可以尝试配合DmGuard中的memory护盾,突破部分窗口内存保护。  
用此函数分配的内存，必须用VirtualFreeEx来释放,以免目标进程内存泄漏.