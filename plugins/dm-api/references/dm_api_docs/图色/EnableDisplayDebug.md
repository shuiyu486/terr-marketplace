函数简介:

开启图色调试模式，此模式会稍许降低图色和文字识别的速度.默认不开启.

函数原型:  
  
long EnableDisplayDebug(enable\_debug)

参数定义:  
  
enable\_debug 整形数: 0 为关闭

              
1 为开启

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.EnableDisplayDebug 1  
dm\_ret = dm.CapturePre("screen.bmp")