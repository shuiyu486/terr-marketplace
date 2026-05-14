函数简介:

设置窗口的标题

函数原型:  
  
long SetWindowText(hwnd,title)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
titie 字符串: 标题

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret =
dm.SetWindowText(hwnd,"test")