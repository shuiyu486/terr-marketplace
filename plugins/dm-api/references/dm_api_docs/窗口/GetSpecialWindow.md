函数简介:

获取特殊窗口

函数原型:  
  
long GetSpecialWindow(flag)

参数定义:

Flag 整形数: 取值定义如下

0 : 获取桌面窗口

1 : 获取任务栏窗口

返回值:

整形数:  
以整型数表示的窗口句柄

示例:

desk\_win = dm.GetSpecialWindow(0)