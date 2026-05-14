函数简介:

得到系统的路径

函数原型:  
  
string GetDir(type)

参数定义:

type 整形数: 取值为以下类型

     0 : 获取当前路径

     1 : 获取系统路径(system32路径)

     2 : 获取windows路径(windows所在路径)

     3 : 获取临时目录路径(temp)

     4 : 获取当前进程(exe)所在的路径

返回值:

字符串:  
返回路径

示例:

path = dm.GetDir(2)