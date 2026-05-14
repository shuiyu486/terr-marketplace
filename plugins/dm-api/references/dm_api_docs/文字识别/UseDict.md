函数简介:

表示使用哪个字库文件进行识别(index范围:0-99)

设置之后，永久生效，除非再次设定

函数原型:  
  
long UseDict(index)

参数定义:  
  
index 整形数:字库编号(0-99)

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.UseDict(1)  
ss = dm.Ocr(0,0,2000,2000,"FFFFFF-000000",1.0)  
dm\_ret = dm.UseDict(0)