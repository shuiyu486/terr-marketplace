函数简介:

关闭当前系统屏幕字体平滑.同时关闭系统的ClearType功能.

函数原型:  
  
long DisableFontSmooth()

参数定义:

返回值:  
  
整形数:  
0 : 失败

1 : 成功

示例:

if dm.CheckFontSmooth()
= 1 then  
   if dm.DisableFontSmooth()
= 1 then  
      MessageBox "关闭了当前系统平滑字体,重启生效"  
      dm.ExitOs 2  
      Delay 2000  
      EndScript  
   end if  
end if  
  
注: 关闭之后要让系统生效，必须重启系统才有效.