函数简介:

向指定的Ini写入信息. 

函数原型:  
  
long WriteIni(section,key,value,file)

参数定义:

section 字符串: 小节名

key 字符串: 变量名.

value 字符串: 变量内容

file 字符串: ini文件名.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.WriteIni
"Global","var1","123","c:\test\_game\cfg.ini"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.WriteIni
"Global","var1","123","cfg.ini"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.