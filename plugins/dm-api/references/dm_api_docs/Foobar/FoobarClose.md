函数简介:

关闭一个Foobar,注意,必须调用此函数来关闭窗口,用SetWindowState也可以关闭,但会造成内存泄漏.

函数原型:  
  
long FoobarClose(hwnd)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口句柄

返回值:  
  
整形数:  
0: 失败

1: 成功

示例:

dm\_ret = dm.FoobarClose(foobar)