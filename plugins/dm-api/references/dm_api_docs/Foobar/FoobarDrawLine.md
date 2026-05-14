函数简介:

在指定的Foobar窗口内部画线条.

函数原型:  
  
long FoobarDrawLine(hwnd,x1,y1,x2,y2,color,style,width)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的  
  
x1 整形数: 左上角X坐标(相对于hwnd客户区坐标)

y1 整形数: 左上角Y坐标(相对于hwnd客户区坐标)

x2 整形数: 右下角X坐标(相对于hwnd客户区坐标)

y2 整形数: 右下角Y坐标(相对于hwnd客户区坐标)

color字符串: 填充的颜色值

style 整形数: 画笔类型. 0为实线. 1为虚线

width 整形数: 线条宽度.

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarDrawLine(foobar,0,0,200,200,"FF0000",1,1)

注:当style为1时，线条宽度必须也是1.否则线条是实线.