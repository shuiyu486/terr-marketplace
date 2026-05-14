函数简介:

运行指定的应用程序.

函数原型:  
  
long RunApp(app\_path,mode)

参数定义:

app\_path 字符串: 指定的可执行程序全路径.

mode 整形数: 取值如下

      0 : 普通模式

      1 : 加强模式

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm.RunApp "c:\windows\notepad.exe",0

dm.RunApp "notepad",1