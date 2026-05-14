函数简介:

设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常点击。

函数原型:  
  
long SetMouseDelay(type,delay)

参数定义:  
  
type 字符串: 鼠标类型,取值有以下

     "normal" : 对应normal鼠标 默认内部延时为 30ms

     "windows": 对应windows 鼠标 默认内部延时为 10ms

     "dx" :     对应dx鼠标 默认内部延时为40ms

delay 整形数: 延时,单位是毫秒

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.SetMouseDelay "dx",10

注 : 此函数影响的接口有LeftClick RightClick MiddleClick LeftDoubleClick