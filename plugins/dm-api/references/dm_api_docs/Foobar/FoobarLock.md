函数简介:

锁定指定的Foobar窗口,不能通过鼠标来移动

函数原型:  
  
long FoobarLock(hwnd)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarLock(foobar)