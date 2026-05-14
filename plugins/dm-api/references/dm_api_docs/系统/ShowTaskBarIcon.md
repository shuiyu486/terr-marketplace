函数简介:

显示或者隐藏指定窗口在任务栏的图标.

函数原型:  
  
long ShowTaskBarIcon(hwnd,is\_show)

参数定义:

hwnd 整形数: 指定的窗口句柄

is\_show 整形数: 0为隐藏,1为显示

返回值:  
  
整形数:  
0 : 失败

1 : 成功

示例:

// 显示  
dm.ShowTaskBarIcon hwnd,1  
  
// 隐藏  
dm.ShowTaskBarIcon hwnd,0