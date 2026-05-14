函数简介:

获取窗口客户区域的宽度和高度

函数原型:  
  
long GetClientSize(hwnd,width,height)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
width 变参指针: 宽度

height 变参指针: 高度

返回值:  
  
整形数:  
0: 失败  
1: 成功

示例:

dm\_ret =
dm.GetClientSize(hwnd,w,h)   
TracePrint "宽度:"&
w &",高度:"& h