函数简介:

设置EnumWindow  EnumWindowByProcess  EnumWindowSuper
FindWindow以及FindWindowEx的最长延时. 内部默认超时是10秒.

函数原型:  
  
long SetEnumWindowDelay(delay)

参数定义:  
  
delay 整形数: 单位毫秒

返回值:

整形数:  
0: 失败

1: 成功

示例:

dm.SetEnumWindowDelay 
300000

注: 有些时候，窗口过多，并且窗口结构过于复杂，可能枚举的时间过长. 那么需要调用这个函数来延长时间。避免漏掉窗口.