函数简介:

识别位图中区域(x1,y1,x2,y2)的文字

函数原型:  
  
string OcrInFile(x1, y1, x2, y2, pic\_name,
color\_format, sim)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
pic\_name 字符串:图片文件名  
color\_format 字符串:颜色格式串.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度,取值范围0.1-1.0

返回值:  
  
字符串:  
返回识别到的字符串

示例:

s = dm.OcrInFile(0,0,2000,2000,"test.bmp","000000-000000",1.0)  
MessageBox s