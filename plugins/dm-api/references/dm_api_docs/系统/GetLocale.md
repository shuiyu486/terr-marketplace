函数简介:

判断当前系统使用的非UNICODE字符集是否是GB2312(简体中文)(由于设计插件时偷懒了,使用的是非UNICODE字符集，导致插件必须运行在GB2312字符集环境下).

函数原型:  
  
long GetLocale()

参数定义:

返回值:  
  
整形数:  
0 : 不是GB2312(简体中文)

1 : 是GB2312(简体中文)

示例:

if dm.GetLocale() = 0 then  
    dm.SetLocale()  
    dm.ExitOs(2)  
end if