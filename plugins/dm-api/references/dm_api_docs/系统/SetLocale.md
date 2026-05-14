函数简介:

设置当前系统的非UNICOD字符集. 会弹出一个字符集选择列表,用户自己选择到简体中文即可.

函数原型:  
  
long SetLocale()

参数定义:

返回值:  
  
整形数:  
0 : 失败

1 : 成功

示例:

if dm.GetLocale() = 0 then  
    dm.SetLocale()  
    dm.ExitOs(2)  
end if