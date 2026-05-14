函数简介:

删除文件.

函数原型:  
  
long DeleteFile(file)

参数定义:

file 字符串: 文件名

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.DeleteFile "c:\123.txt"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.DeleteFile "123.txt"