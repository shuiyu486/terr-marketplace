函数简介:

根据两组设定条件来枚举指定窗口.

函数原型:  
  
string
EnumWindowSuper(spec1,flag1,type1,spec2,flag2,type2,sort)

参数定义:

spec1 字符串: 查找串1. (内容取决于flag1的值)

flag1整形数: 取值如下:

   0表示spec1的内容是标题

   1表示spec1的内容是程序名字. (比如notepad)

   2表示spec1的内容是类名

   3表示spec1的内容是程序路径.(不包含盘符,比如\windows\system32)

   4表示spec1的内容是父句柄.(十进制表达的串)

   5表示spec1的内容是父窗口标题

   6表示spec1的内容是父窗口类名

   7表示spec1的内容是顶级窗口句柄.(十进制表达的串)

   8表示spec1的内容是顶级窗口标题

   9表示spec1的内容是顶级窗口类名

type1 整形数: 取值如下

0精确判断

1模糊判断

spec2 字符串: 查找串2. (内容取决于flag2的值)

flag2 整形数: 取值如下:

   0表示spec2的内容是标题

   1表示spec2的内容是程序名字. (比如notepad)

   2表示spec2的内容是类名

   3表示spec2的内容是程序路径.(不包含盘符,比如\windows\system32)

   4表示spec2的内容是父句柄.(十进制表达的串)

   5表示spec2的内容是父窗口标题

   6表示spec2的内容是父窗口类名

   7表示spec2的内容是顶级窗口句柄.(十进制表达的串)

   8表示spec2的内容是顶级窗口标题

   9表示spec2的内容是顶级窗口类名

type2  整形数: 取值如下

0精确判断

1模糊判断

sort  整形数: 取值如下

0不排序.

1对枚举出的窗口进行排序,按照窗口打开顺序.

返回值:  
  
字符串:  
返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"

示例:

hwnds = dm.EnumWindowSuper("记事本",0,1,"notepad",1,0,0) 

hwnds = split(hwnds,",")

转换为数组后,就可以处理了

这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))