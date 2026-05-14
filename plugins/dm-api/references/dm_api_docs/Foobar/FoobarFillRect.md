函数简介:

在指定的Foobar窗口内部填充矩形

函数原型:  
  
long FoobarFillRect(hwnd,x1,y1,x2,y2,color)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的  
  
x1 整形数: 左上角X坐标(相对于hwnd客户区坐标)

y1 整形数: 左上角Y坐标(相对于hwnd客户区坐标)

x2 整形数: 右下角X坐标(相对于hwnd客户区坐标)

y2 整形数: 右下角Y坐标(相对于hwnd客户区坐标)

color字符串: 填充的颜色值

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.FoobarFillRect(foobar,0,0,200,200,"FF0000")