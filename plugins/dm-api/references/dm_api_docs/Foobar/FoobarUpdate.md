函数简介:

刷新指定的Foobar窗口

函数原型:  
  
long FoobarUpdate(hwnd)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarUpdate(foobar)

注意： 所有绘制完成以后,必须通过调用此函数来刷新窗口,否则窗口内容不会改变.