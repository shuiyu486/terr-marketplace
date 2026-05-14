函数简介:

在不解绑的情况下,切换绑定窗口.(必须是同进程窗口)

函数原型:  
  
long SwitchBindWindow(hwnd)

参数定义:

hwnd 整形数: 需要切换过去的窗口句柄

返回值:

整形数:  
0: 失败  
1: 成功

示例:

// 绑定为后台  
dm\_ret = dm.BindWindow(hwnd,"dx","dx","dx",101)  
// 切换  
hwnd1 = 111  
dm.SwitchBindWindow(hwnd1)

注:此函数一般用在绑定以后，窗口句柄改变了的情况。如果必须不解绑，那么此函数就很有用了。