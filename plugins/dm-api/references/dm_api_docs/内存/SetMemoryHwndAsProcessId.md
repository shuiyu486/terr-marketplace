函数简介:

设置是否把所有内存接口函数中的窗口句柄当作进程ID,以支持直接以进程ID来使用内存接口.

函数原型:  
  
long SetMemoryHwndAsProcessId(en)

参数定义:  
  
en 整形数: 取值如下  
            
0 : 关闭 
1 : 开启

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

dm.SetMemoryHwndAsProcessId 1

注: 默认是当作窗口句柄.