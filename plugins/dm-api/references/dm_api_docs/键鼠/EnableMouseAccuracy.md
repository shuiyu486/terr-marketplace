函数简介:

设置当前系统鼠标的精确度开关. 如果所示。 此接口仅仅对前台MoveR接口起作用.

函数原型:  
  
long EnableMouseAccuracy(enable)

参数定义:  
  
enable整形数: 0 关闭指针精确度开关.  1打开指针精确度开关. 一般推荐关闭.

返回值:

整形数:  
设置之前的精确度开关.

示例:

dm.SetMouseAccuracy 0