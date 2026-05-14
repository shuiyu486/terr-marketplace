函数简介:

设置窗口客户区域的宽度和高度

函数原型:  
  
long SetClientSize(hwnd,width,height)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
width 整形数: 宽度

height 整形数: 高度

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret =
dm.SetClientSize(hwnd,800,600)