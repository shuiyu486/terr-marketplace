函数简介:

获取当前CPU类型(intel或者amd).

函数原型:  
  
long GetCpuType()

参数定义:

返回值:  
  
整形数:  
0 : 未知

1 : Intel cpu

2 : AMD cpu

示例:

if dm.GetCpuType() <> 1 then  
    MessageBox "当前系统CPU不是intel
cpu,不支持!"  
    EndScript  
end if