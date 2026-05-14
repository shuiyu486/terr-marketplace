函数简介:

检测当前系统是否有开启屏幕字体平滑.

函数原型:  
  
long CheckFontSmooth()

参数定义:

返回值:  
  
整形数:  
0 : 系统没开启平滑字体.

1 : 系统有开启平滑字体.

示例:

if dm.CheckFontSmooth () = 1 then  
    TracePrint
"当前系统有开启平滑字体"  
end if