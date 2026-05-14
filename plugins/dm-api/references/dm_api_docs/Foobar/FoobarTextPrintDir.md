函数简介:

设置滚动文本区的文字输出方向,默认是0

函数原型:  
  
long FoobarTextPrintDir(hwnd,dir)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

dir 整形数: 0 表示向下输出

          : 1 表示向上输出

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarTextPrintDir(foobar,1)