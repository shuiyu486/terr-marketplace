函数简介:

根据指定的ini文件,枚举此ini中所有的Section(小节名) 可支持加密文件

函数原型:  
  
string EnumIniSectionPwd(file,pwd)

参数定义:

file 字符串: ini文件名.  
pwd 字符串: 密码

返回值:  
  
字符串:  
每个小节名用"|"来连接，如果没有小节，则返回空字符串. 比如"aaa|bbb|ccc"

示例:  
  
// 绝对路径  
dm\_ret = dm.EnumIniSectionPwd("c:\test\_game\cfg.ini","123")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm\_ret = dm.EnumIniSectionPwd("cfg.ini","123")

if len(dm\_ret) > 0 then  
sections = split(dm\_ret,"|")  
count = ubound(sections) + 1  
index = 0  
Do While index < count  
     TracePrint sections(index)  
     index = index +
1  
Loop

end if

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果文件没加密，也可以正常读取.