函数简介:

开启当前系统屏幕字体平滑.同时开启系统的ClearType功能.

函数原型:  
  
long EnableFontSmooth()

参数定义:

返回值:  
  
整形数:  
0 : 失败

1 : 成功

示例:

if dm.CheckFontSmooth()
= 0 then  
   if dm.EnableFontSmooth()
= 1 then  
      MessageBox "开启了当前系统平滑字体,重启生效"  
      dm.ExitOs 2  
      Delay 2000  
      EndScript  
   end if  
end if  
  
注: 开启之后要让系统生效，必须重启系统才有效.