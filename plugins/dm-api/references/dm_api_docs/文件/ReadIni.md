函数简介:

从Ini中读取指定信息.

函数原型:  
  
string ReadIni(section,key,file)

参数定义:

section 字符串: 小节名

key 字符串: 变量名.

file 字符串: ini文件名.

返回值:  
  
字符串:  
字符串形式表达的读取到的内容

示例:  
  
// 绝对路径  
Text =
dm.ReadIni("Global","var1","c:\test\_game\cfg.ini")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
Text = dm.ReadIni("Global","var1","cfg.ini")

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.