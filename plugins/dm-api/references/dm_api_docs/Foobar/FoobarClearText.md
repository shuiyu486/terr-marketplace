函数简介:

清除指定的Foobar滚动文本区

函数原型:  
  
long FoobarClearText(hwnd)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

返回值:

整形数 :  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarClearText(foobar)