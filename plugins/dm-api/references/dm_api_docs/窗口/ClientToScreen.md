函数简介:

把窗口坐标转换为屏幕坐标

函数原型:  
  
long ClientToScreen(hwnd,x,y)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄

x 变参指针: 窗口X坐标

y 变参指针: 窗口Y坐标

返回值:

整形数:  
0: 失败  
1: 成功

示例:

x = 0:y = 0   
dm\_ret = dm.ClientToScreen(hwnd,x,y)