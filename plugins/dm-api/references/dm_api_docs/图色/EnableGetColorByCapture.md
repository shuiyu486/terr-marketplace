函数简介:

允许调用GetColor GetColorBGR GetColorHSV 以及 CmpColor时，以截图的方式来获取颜色。 默认关闭.

函数原型:  
  
long EnableGetColorByCapture(enable)

参数定义:

enable 整形数: 0 关闭

        
1 打开

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

dm.EnableGetColorByCapture 1  
TracePrint dm.GetColor(300,300)

注 : 某些窗口上，可能GetColor会获取不到颜色，可以尝试此接口.