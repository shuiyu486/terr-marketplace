函数简介:

获取指定的按键状态.(前台信息,不是后台)

函数原型:  
  
long GetKeyState(vk\_code)

参数定义:  
  
vk\_code 整形数:虚拟按键码

返回值:

整形数:  
0:弹起  
1:按下

示例:

TracePrint dm.GetKeyState(13)