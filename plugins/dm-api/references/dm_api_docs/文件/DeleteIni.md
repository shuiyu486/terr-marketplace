函数简介:

删除指定的ini小节. 

函数原型:  
  
long DeleteIni(section,key,file)

参数定义:

section 字符串: 小节名

key 字符串: 变量名. 如果这个变量为空串，则删除整个section小节.

file 字符串: ini文件名.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.DeleteIni "Global","var1" ,"c:\test\_game\cfg.ini"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.DeleteIni "Global","" ,"cfg.ini"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.