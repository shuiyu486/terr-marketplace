函数简介:

判断当前系统是否是64位操作系统

函数原型:  
  
long Is64Bit()

参数定义:

返回值:

整形数:  
0 : 不是64位系统  
1 : 是64位系统

示例:

if dm.Is64Bit() = 1 then  
    MessageBox "64位系统"  
else  
    MessageBox "不是64位系统"  
end if