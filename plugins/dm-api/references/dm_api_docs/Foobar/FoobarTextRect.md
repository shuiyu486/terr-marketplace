函数简介:

设置指定Foobar窗口的滚动文本框范围,默认的文本框范围是窗口区域

函数原型:  
  
long FoobarTextRect(hwnd,x,y,w,h)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

x 整形数: x坐标

y 整形数: y坐标

w 整形数: 宽度

h 整形数: 高度

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarTextRect(foobar,10,10,100,200)