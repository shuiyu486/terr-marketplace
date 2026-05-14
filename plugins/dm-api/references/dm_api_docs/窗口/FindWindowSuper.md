函数简介:

根据两组设定条件来查找指定窗口.

函数原型:  
  
long
FindWindowSuper(spec1,flag1,type1,spec2,flag2,type2)

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

返回值:  
  
整形数:  
整形数表示的窗口句柄，没找到返回0

示例:

hwnd = dm.FindWindowSuper("记事本",0,1,"notepad",1,0)