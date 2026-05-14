函数简介:

向指定的Foobar窗口区域内输出滚动文字

函数原型:  
  
long FoobarPrintText(hwnd,text,color)

参数定义:  
  
hwnd整形数: 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来

text字符串: 文本内容

color字符串: 文本颜色

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.FoobarPrintText(foobar,"大漠测试","ff0000")

// 用红色文字向滚动区域输出文字信息