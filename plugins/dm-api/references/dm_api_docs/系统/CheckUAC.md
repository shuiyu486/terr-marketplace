函数简介:

检测当前系统是否有开启UAC(用户账户控制).

函数原型:  
  
long CheckUAC()

参数定义:

返回值:

整形数:  
0 : 没开启UAC

1 : 开启了UAC

示例:

if dm.CheckUAC() = 1 then  
    TracePrint "当前系统开启了用户账户控制"  
end if

注: 只有WIN7 WIN8 VISTA WIN2008以及以上系统才有UAC设置