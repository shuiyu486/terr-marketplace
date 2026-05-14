函数简介:

设置是否弹出汇编功能中的错误提示,默认是打开.

函数原型:  
  
long SetShowAsmErrorMsg(show)

参数定义:

show 整形数: 0表示不打开,1表示打开

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.SetShowAsmErrorMsg(0)