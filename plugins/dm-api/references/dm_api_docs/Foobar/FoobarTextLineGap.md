函数简介:

设置滚动文本区的文字行间距,默认是3

函数原型:  
  
long FoobarTextLineGap(hwnd,line\_gap)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

line\_gap 整形数: 文本行间距

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.FoobarTextLineGap(foobar,5)