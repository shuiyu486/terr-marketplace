函数简介:

获取窗口在屏幕上的位置

函数原型:  
  
long GetWindowRect(hwnd,x1,y1,x2,y2)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
x1 变参指针: 返回窗口左上角X坐标

y1 变参指针: 返回窗口左上角Y坐标

x2 变参指针: 返回窗口右下角X坐标

y2 变参指针: 返回窗口右下角Y坐标

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret =
dm.GetWindowRect(hwnd,x1,y1,x2,y2)