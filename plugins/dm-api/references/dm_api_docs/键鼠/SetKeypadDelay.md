函数简介:

设置按键时,键盘按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常按键。

函数原型:  
  
long SetKeypadDelay(type,delay)

参数定义:  
  
type 字符串: 键盘类型,取值有以下

     "normal" : 对应normal键盘  默认内部延时为30ms

     "windows": 对应windows 键盘 默认内部延时为10ms

     "dx" :     对应dx 键盘 默认内部延时为50ms

delay 整形数: 延时,单位是毫秒

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.SetKeypadDelay
"dx",10

注 : 此函数影响的接口有KeyPress