函数简介:

在指定的Foobar窗口绘制文字

函数原型:  
  
long FoobarDrawText(hwnd,x,y,w,h,text,color,align)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的  
  
x整形数: 左上角X坐标(相对于hwnd客户区坐标)

y整形数: 左上角Y坐标(相对于hwnd客户区坐标)

w整形数: 矩形区域的宽度

h整形数: 矩形区域的高度

text字符串: 字符串

color字符串: 文字颜色值

align 整形数: 取值定义如下

1 : 左对齐

2 : 中间对齐

4 : 右对齐

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.FoobarDrawText(foobar,0,0,200,30,"测试","FF0000",1)