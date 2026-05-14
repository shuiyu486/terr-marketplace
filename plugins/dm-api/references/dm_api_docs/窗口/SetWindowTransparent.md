函数简介:

设置窗口的透明度

函数原型:  
  
long SetWindowTransparent(hwnd,trans)

参数定义:  
  
hwnd 整形数: 指定的窗口句柄  
  
trans 整形数: 透明度
取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明)

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret =
dm.SetWindowTransparent(hwnd,200)

注 :  此接口不支持WIN98