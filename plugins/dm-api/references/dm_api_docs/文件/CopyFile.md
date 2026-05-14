函数简介:

拷贝文件.

函数原型:  
  
long CopyFile(src\_file,dst\_file,over)

参数定义:

src\_file 字符串: 原始文件名

dst\_file 字符串: 目标文件名.

over整形数: 取值如下,  
           
0 : 如果dst\_file文件存在则不覆盖返回.  
           
1 : 如果dst\_file文件存在则覆盖.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.CopyFile "c:\123.txt","d:\456.txt",1  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.CopyFile "123.txt","456.txt",1