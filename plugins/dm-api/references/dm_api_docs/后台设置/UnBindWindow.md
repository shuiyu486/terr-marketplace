函数简介:

解除绑定窗口,并释放系统资源.一般在OnScriptExit调用

函数原型:  
  
long UnBindWindow()

参数定义:

返回值:

整形数:  
0: 失败  
1: 成功

示例:

Sub OnScriptExit()  
    dm\_ret =
dm.UnBindWindow()   
End Sub