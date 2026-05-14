函数简介:

根据指定进程以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口

函数原型:  
  
string EnumWindowByProcess(process\_name,title,class\_name,filter)

参数定义:

process\_name 字符串: 进程映像名.比如(svchost.exe). 此参数是精确匹配,但不区分大小写.

title 字符串: 窗口标题. 此参数是模糊匹配.

class\_name 字符串: 窗口类名. 此参数是模糊匹配.

filter 整形数: 取值定义如下

1 : 匹配窗口标题,参数title有效

2 : 匹配窗口类名,参数class\_name有效

4 : 只匹配指定映像的所对应的第一个进程. 可能有很多同映像名的进程，只匹配第一个进程的.

8 : 匹配父窗口为0的窗口,即顶级窗口

16 : 匹配可见的窗口

32 : 匹配出的窗口按照窗口打开顺序依次排列

这些值可以相加,比如4+8+16

返回值:

字符串:  
返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"

示例:

hwnds = dm.EnumWindowByProcess("game.exe","天龙八部","",1+8+16)

这句是获取到所有标题栏中有"天龙八部"这个字符串的窗口句柄集合,并且所在进程是"game.exe"指定的进程集合.

hwnds = split(hwnds,",")

转换为数组后,就可以处理了

这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))