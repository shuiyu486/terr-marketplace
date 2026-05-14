函数简介:

解锁指定的Foobar窗口,可以通过鼠标来移动

函数原型:  
  
long FoobarUnlock(hwnd)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarUnlock(foobar)