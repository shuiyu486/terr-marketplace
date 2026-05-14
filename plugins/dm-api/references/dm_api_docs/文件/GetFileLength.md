函数简介:

获取指定的文件长度.

函数原型:  
  
long GetFileLength(file)

参数定义:

file 字符串: 文件名

返回值:  
  
整形数:  
文件长度(字节数)

示例:  
  
// 绝对路径  
TracePrint dm.GetFileLength("c:\123.txt")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
TracePrint dm.GetFileLength("123.txt")