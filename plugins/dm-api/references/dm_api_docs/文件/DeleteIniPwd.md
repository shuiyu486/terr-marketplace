函数简介:

删除指定的ini小节.支持加密文件

函数原型:  
  
long DeleteIniPwd(section,key,file,pwd)

参数定义:

section 字符串: 小节名

key 字符串: 变量名. 如果这个变量为空串，则删除整个section小节.

file 字符串: ini文件名.

pwd 字符串: 密码.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.DeleteIniPwd
"Global","var1","c:\test\_game\cfg.ini","1234"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.DeleteIniPwd
"Global","","cfg.ini","1234"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果此文件没加密，调用此函数会自动加密.