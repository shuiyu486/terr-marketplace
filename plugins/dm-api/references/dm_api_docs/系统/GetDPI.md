函数简介:

判断当前系统的DPI(文字缩放)是不是100%缩放.

函数原型:  
  
long GetDPI()

参数定义:

返回值:  
  
整形数:  
0 : 不是

1 : 是

示例:

if dm.GetDPI() = 0 then  
    MessageBox "当前系统文字缩放不是100%,请设置为100%"  
    EndScript  
end if