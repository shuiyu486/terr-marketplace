函数简介:

移动指定窗口到指定位置

函数原型:  
  
long MoveWindow(hwnd,x,y)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
x 整形数: X坐标

y 整形数: Y坐标

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm.MoveWindow hwnd,-10,-10