函数简介:

根据指定的进程名字，来查找可见窗口.

函数原型:  
  
long FindWindowByProcess(process\_name,class,title)

参数定义:  
  
process\_name 字符串: 进程名. 比如(notepad.exe).这里是精确匹配,但不区分大小写.  
  
class 字符串: 窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配.

title 字符串: 窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配.

返回值:  
  
整形数:  
整形数表示的窗口句柄，没找到返回0

示例:

hwnd = dm.FindWindowByProcess("noteapd.exe","","记事本")