函数简介:

抓取指定区域(x1, y1, x2, y2)的图像,保存为file(JPG压缩格式)

函数原型:  
  
long CaptureJpg(x1, y1, x2,
y2, file, quality)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
file 字符串:保存的文件名,保存的地方一般为SetPath中设置的目录

     当然这里也可以指定全路径名.  
quality 整形数: jpg压缩比率(1-100) 越大图片质量越好

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.CaptureJpg(0,0,2000,2000,"screen.jpg",50)