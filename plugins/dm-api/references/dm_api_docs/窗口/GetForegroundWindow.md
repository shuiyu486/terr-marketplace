函数简介:

获取顶层活动窗口,可以获取到按键自带插件无法获取到的句柄

函数原型:  
  
long GetForegroundWindow()

参数定义:

返回值:

整形数:  
返回整型表示的窗口句柄

示例:

hwnd = dm.GetForegroundWindow()