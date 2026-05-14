函数简介:

根据指定的ini文件以及section,枚举此section中所有的key名

函数原型:  
  
string EnumIniKey(section,file)

参数定义:

section 字符串: 小节名. (不可为空)  
file 字符串: ini文件名.

返回值:  
  
字符串:  
每个key用"|"来连接，如果没有key，则返回空字符串. 比如"aaa|bbb|ccc"

示例:  
  
// 绝对路径  
dm\_ret = dm.EnumIniKey("aaa","c:\test\_game\cfg.ini")  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm\_ret = dm.EnumIniKey("aaa","cfg.ini")

if len(dm\_ret) > 0 then  
keys = split(dm\_ret,"|")  
count = ubound(keys) + 1  
index = 0  
Do While index < count  
     TracePrint
keys(index)  
     index = index +
1  
Loop

end if

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.  
另外,此函数无法枚举没有section的key.