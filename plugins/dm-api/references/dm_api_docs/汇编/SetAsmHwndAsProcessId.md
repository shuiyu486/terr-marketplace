函数简介:

使用AsmCall时的hwnd参数当作进程pid. 注:仅对AsmCall的模式1起作用,因为其它模式都需要窗口.

函数原型:  
  
long SetAsmHwndAsProcessId(enable)

参数定义:

enable 整形数: 0关闭,1打开

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.SetAsmHwndAsProcessId 1  
dm.AsmCall pid,1