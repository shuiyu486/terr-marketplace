函数简介:

从指定的文件读取内容.

函数原型:  
  
string ReadFile(file)

参数定义:

file 字符串: 文件

返回值:  
  
字符串:  
读入的文件内容

示例:  
  
// 绝对路径  
TracePrint dm.ReadFile("c:\123.txt")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
TracePrint dm.ReadFile("123.txt")