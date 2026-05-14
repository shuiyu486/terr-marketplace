函数简介:

设置是否弹出错误信息,默认是打开.

函数原型:  
  
long SetShowErrorMsg(show)

参数定义:

show 整形数: 0表示不打开,1表示打开

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.SetShowErrorMsg(0)