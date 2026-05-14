函数简介:

同FindStrEx

函数原型:  
  
string FindStrFastEx(x1,y1,x2,y2,string,color\_format,sim)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
string 字符串:待查找的字符串, 可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串  
color\_format 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度,取值范围0.1-1.0

返回值:

字符串:  
返回所有找到的坐标集合,格式如下:  
"id,x0,y0|id,x1,y1|......|id,xn,yn"  
比如"0,100,20|2,30,40" 表示找到了两个,第一个,对应的是序号为0的字符串,坐标是(100,20),第二个是序号为2的字符串,坐标(30,40)

示例:

dm\_ret = dm.FindStrFastEx(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",0.9)  
If len(dm\_ret) > 0 Then  
   ss
= split(dm\_ret,"|")  
   index = 0  
   count = UBound(ss) + 1  
   Do While index < count  
      TracePrint ss(index)  
      sss = split(ss(index),",")  
      id = int(sss(0))  
      x = int(sss(1))  
      y = int(sss(2))  
      dm.MoveTo x,y  
      Delay 1000  
      index =
index+1  
   Loop  
End If

注: 此函数比FindStrEx要快很多，尤其是在字库很大时，或者模糊识别时，效果非常明显。  
推荐使用此函数。

另外由于此函数是只识别待查找的字符，所以可能会有如下情况出现问题。

比如 字库中有"张和三" 一共3个字符数据，然后待识别区域里是"张和三",如果用FindStrEx查找  
"张三"肯定是找不到的，但是用FindStrFastEx却可以找到，因为"和"这个字符没有列入查找计划中  
所以，在使用此函数时，也要特别注意这一点。