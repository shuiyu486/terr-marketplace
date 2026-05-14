函数简介:

判断指定文件是否存在.

函数原型:  
  
long IsFileExist(file)

参数定义:

file 字符串: 文件名

返回值:  
  
整形数:  
0 : 不存在  
1 : 存在

示例:  
  
// 绝对路径  
TracePrint dm.IsFileExist("c:\123.txt")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
TracePrint dm.IsFileExist("123.txt")