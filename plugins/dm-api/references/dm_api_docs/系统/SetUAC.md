函数简介:

设置当前系统的UAC(用户账户控制).

函数原型:  
  
long SetUAC(enable)

参数定义:

enable 整形数: 取值如下

       0 : 关闭UAC  
       1 : 开启UAC

返回值:  
  
整形数:  
0 : 操作失败

1 : 操作成功

示例:

if dm.SetUAC(0) = 1 then  
    TracePrint "成功关闭了当前系统UAC设置"  
end if

注: 只有WIN7 WIN8 VISTA WIN2008以及以上系统才有UAC设置. 关闭UAC以后，必须重启系统才会生效.

如果关闭了UAC，那么默认启动所有应用程序都是管理员权限，就不会再发生绑定失败这样的尴尬情况了.