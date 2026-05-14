函数简介:

判断当前CPU是否支持vt,并且是否在bios中开启了vt. 仅支持intel的CPU.

函数原型:  
  
long IsSurrpotVt()

参数定义:

返回值:

整形数:  
0 : 当前cpu不是intel的cpu,或者当前cpu不支持vt,或者bios中没打开vt.  
1 : 支持

示例:

if dm.IsSurrpotVt() = 1 then  
    MessageBox "当前系统可以开启vt功能"  
else  
    MessageBox "不支持vt"  
end if