函数简介:

向绑定的窗口发送文本数据.必须配合dx.public.input.ime属性.

函数原型:  
  
long SendStringIme(str)

参数定义:  
  
str 字符串: 发送的文本数据

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret = dm.BindWindowEx(hwnd,"normal","normal","normal","dx.public.input.ime",0)  
dm.SendStringIme "我是来测试的"