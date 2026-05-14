函数简介:

设置指定Foobar窗口的字体

函数原型:  
  
long FoobarSetFont(hwnd,font\_name,size,flag)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

font\_name字符串: 系统字体名,注意,必须保证系统中有此字体

size整形数: 字体大小

flag整形数: 取值定义如下

0 : 正常字体

1 : 粗体

2 : 斜体

4 : 下划线

文字可以是以上的组合 比如粗斜体就是1+2,斜体带下划线就是:2+4等.

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.FoobarSetFont(foobar,"宋体",25,2+4)