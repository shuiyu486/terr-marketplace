函数简介:

获取范围(x1,y1,x2,y2)颜色的均值,返回格式"RRGGBB"

函数原型:  
  
string GetAveRGB(x1,y1,x2,y2)

参数定义:  
  
x1 整形数: 左上角X

y1 整形数: 左上角Y

x2 整形数: 右下角X

y2 整形数: 右下角Y

返回值:

字符串:  
颜色字符串

示例:

color = dm.GetAveRGB(30,30,100,100)  
MessageBox color