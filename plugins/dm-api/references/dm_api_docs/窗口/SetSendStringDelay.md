函数简介:

设置SendString和SendString2的每个字符之间的发送间隔.  有些窗口必须设置延迟才可以正常发送. 否则可能会顺序错乱.

函数原型:  
  
long SetSendStringDelay(delay)

参数定义:  
  
delay 整形数: 大于等于0的延迟数值. 单位是毫秒. 默认是0

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm.SetSendStringDelay 100  
dm.SendString hwnd,"abcd"