函数简介:

设置指定Foobar窗口的是否透明

函数原型:  
  
long FoobarSetTrans(hwnd,is\_trans,color,sim)

参数定义:  
  
hwnd 整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

is\_trans 整形数: 是否透明. 0为不透明(此时,color和sim无效)，1为透明.

color 字符串: 透明色(RRGGBB)

sim 双精度浮点数: 透明色的相似值 0.1-1.0

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

foobar=dm.CreateFoobarRoundRect(hwnd,1,1,300,300,100,100)

dm\_ret = dm.FoobarSetFont(foobar,"宋体",50,0)

dm.FoobarSetTrans foobar,1,"000000",1.0

do

   dm\_ret = dm.FoobarFillRect(foobar,0,0,300,300,"000000")

   dm\_ret = dm.FoobarDrawText(foobar,0,0,300,100,"测试","FF0000",1)

   dm.foobarupdate foobar

   delay 100

Loop

EndScript

注: 调用此接口，最好打开windows的dwm. 否则可能会卡.