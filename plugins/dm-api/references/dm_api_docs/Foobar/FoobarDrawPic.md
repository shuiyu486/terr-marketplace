函数简介:

在指定的Foobar窗口绘制图像

函数原型:  
  
long FoobarDrawPic(hwnd,x,y,pic\_name,trans\_color)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的  
  
x整形数: 左上角X坐标(相对于hwnd客户区坐标)

y整形数: 左上角Y坐标(相对于hwnd客户区坐标)

pic\_name字符串: 图像文件名 [如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制](mailto:如果第一个字符是@,则采用指针方式.%20@后面是指针地址和大小.%20必须是十进制).
具体看下面的例子

trans\_color字符串: 图像透明色

返回值:

整形数 :  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.FoobarDrawPic(foobar,0,0,"menu.bmp","FF0000")  
  
dm\_ret = dm.FoobarDrawPic(foobar,0,0,"@32432525,23435","FF0000")