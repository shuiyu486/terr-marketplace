函数简介:

设置系统的分辨率 系统色深

函数原型:  
  
long SetScreen(width,height,depth)

参数定义:

width 整形数: 屏幕宽度

height 整形数: 屏幕高度

depth 整形数: 系统色深

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret = dm.SetScreen(1024,768,16)