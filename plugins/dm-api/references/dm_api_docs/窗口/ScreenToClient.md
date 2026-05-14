函数简介:

把屏幕坐标转换为窗口坐标

函数原型:  
  
long ScreenToClient(hwnd,x,y)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
x 变参指针: 屏幕X坐标

y 变参指针: 屏幕Y坐标

返回值:

整形数:  
0: 失败  
1: 成功

示例:

x = 100:y = 100   
dm\_ret = dm.ScreenToClient(hwnd,x,y)