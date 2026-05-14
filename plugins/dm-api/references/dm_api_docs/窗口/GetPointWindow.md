函数简介:

获取给定坐标的可见窗口句柄,可以获取到按键自带的插件无法获取到的句柄

函数原型:  
  
long GetPointWindow(x,y)

参数定义:

X 整形数: 屏幕X坐标

Y 整形数: 屏幕Y坐标

返回值:

整形数:  
返回整型表示的窗口句柄

示例:

hwnd = dm.GetPointWindow(100,100)