函数简介:

修改指定的窗口所在进程的地址的读写属性,修改为可读可写可执行.

函数原型:  
  
long VirtualProtectEx(hwnd,addr,size,type,old\_protect)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr 长整形数: 需要修改的地址

size **整形数**: 需要修改的地址大小.

type **整形数**: 修改的地址读写属性类型，取值如下:  
            
0 : 可读可写可执行,此时old\_protect参数无效  
            
1 : 修改为old\_protect指定的读写属性  
old\_protect**整形数**: 指定的读写属性

返回值:

整形数:  
0 : 失败  
1 : 修改之前的读写属性

示例:

// 修改地址&H400000为可读可写可执行,并把修改之前的读写属性保存  
old\_protect = dm.VirtualProtectEx(hwnd,&H400000,5,0,0)  
if old\_protect <> 0 then  
     dm.AsmClear  
     dm.AsmAdd
"lea eax,[400000]"  
     dm.AsmAdd
"mov dword ptr[eax],0"  
     dm.AsmCall
hwnd,1  
    
dm.VirtualProtectEx hwnd,&H400000,5,1,old\_protect  
end if  
  
注:如果正常方式无法修改内存的读写属性,可以尝试配合DmGuard中的memory护盾,突破部分窗口内存保护。