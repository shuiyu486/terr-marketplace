函数简介:

移动文件.

函数原型:  
  
long MoveFile(src\_file,dst\_file)

参数定义:

src\_file 字符串: 原始文件名

dst\_file 字符串: 目标文件名.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.MoveFile "c:\123.txt","d:\456.txt"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.MoveFile "123.txt","456.txt"