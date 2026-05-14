函数简介:

向指定文件追加字符串.

函数原型:  
  
long WriteFile(file,content)

参数定义:

file 字符串: 文件

content 字符串: 写入的字符串.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.WriteFile "c:\123.txt","哈哈哈"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.WriteFile "123.txt","哈哈哈"