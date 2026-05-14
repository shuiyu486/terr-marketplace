函数简介:

获取绑定窗口的fps. (即时fps,不是平均fps).

要想获取fps,那么图色模式必须是dx模式的其中一种.  比如dx.graphic.3d  dx.graphic.opengl等.

函数原型:  
  
long GetFps()

参数定义:

返回值:

整形数: fps

示例:

fps = dm.GetFps()