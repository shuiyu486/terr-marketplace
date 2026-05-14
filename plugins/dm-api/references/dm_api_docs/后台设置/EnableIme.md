函数简介:

设置是否关闭绑定窗口所在进程的输入法.

函数原型:  
  
long EnableIme(enable)

参数定义:

enable 整形数: 1 开启  
0 关闭

返回值:

整形数:  
0: 失败  
1: 成功

示例:

// 绑定为后台  
dm\_ret = dm.BindWindow(hwnd,"dx","dx","dx",101)  
…  
// 关闭输入法  
dm.EnableIme 0   
  
…  
// 再开启输入法  
dm.EnableIme 1

注: 此函数必须在绑定后调用才有效果.