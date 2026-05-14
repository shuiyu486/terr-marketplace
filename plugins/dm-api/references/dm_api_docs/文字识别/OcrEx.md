函数简介:

识别屏幕范围(x1,y1,x2,y2)内符合color\_format的字符串,并且相似度为sim,sim取值范围(0.1-1.0),

这个值越大越精确,越大速度越快,越小速度越慢,请斟酌使用!

这个函数可以返回识别到的字符串，以及每个字符的坐标.

函数原型:  
  
string OcrEx(x1,y1,x2,y2,color\_format,sim)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
color\_format 字符串:颜色格式串.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度,取值范围0.1-1.0

返回值:

字符串:  
返回识别到的字符串 格式如  "字符0$x0$y0|…|字符n$xn$yn"

示例:

和Ocr函数相同，只是结果处理有所不同
如下

dm\_ret = dm.OcrEx(0,0,2000,2000,"ffffff|000000",1.0)  
ss = split(dm\_ret,"|")  
index = 0  
count = UBound(ss) + 1  
Do While index < count  
   TracePrint
ss(index)  
   sss
= split(ss(index),"$")  
   ocr\_s
= int(sss(0))  
   x = int(sss(1))  
   y = int(sss(2))  
   TracePrint
ocr\_s & ","&x&","&y  
   index = index+1  
Loop

注: OcrEx不再像Ocr一样,支持换行分割了.