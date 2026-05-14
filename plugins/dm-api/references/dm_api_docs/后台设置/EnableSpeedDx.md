函数简介:

设置是否开启高速dx键鼠模式。 默认是关闭.

函数原型:  
  
long EnableSpeedDx(enable)

参数定义:

enable 整形数: 0 关闭  
1 开启

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm.EnableSpeedDx 1

注: 此函数开启的后果就是，所有dx键鼠操作将不会等待，适用于某些特殊的场合(比如避免窗口无响应导致宿主进程也卡死的问题).  
EnableMouseSync和EnableKeyboardSync开启以后，此函数就无效了.  
此函数可能在部分窗口下会有副作用，谨慎使用!!