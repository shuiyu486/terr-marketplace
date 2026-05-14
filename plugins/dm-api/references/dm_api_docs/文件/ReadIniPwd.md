函数简介:

从Ini中读取指定信息.可支持加密文件  

函数原型:  
  
string ReadIniPwd(section,key,file,pwd)

参数定义:

section 字符串: 小节名

key 字符串: 变量名.

file 字符串: ini文件名.

pwd 字符串: 密码

返回值:  
  
字符串:  
字符串形式表达的读取到的内容

示例:  
  
// 绝对路径  
Text = dm.ReadIniPwd("Global","var1","c:\test\_game\cfg.ini","1234")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
Text = dm.ReadIniPwd("Global","var1","cfg.ini","1234")

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果文件没加密，也可以正常读取.