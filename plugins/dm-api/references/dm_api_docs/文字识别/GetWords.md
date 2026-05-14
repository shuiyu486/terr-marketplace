函数简介:

根据指定的范围,以及设定好的词组识别参数(一般不用更改,除非你真的理解了)

识别这个范围内所有满足条件的词组. 比较适合用在未知文字的情况下,进行不定识别.

函数原型:  
  
string GetWords(x1, y1, x2,
y2, color, sim)

参数定义:  
  
x1 整形数:左上角X坐标  
y1 整形数:左上角Y坐标  
x2 整形数:右下角X坐标  
y2 整形数:右下角Y坐标  
color 字符串: 颜色格式串.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度 0.1-1.0

返回值:

字符串:  
识别到的格式串,要用到专用函数来解析

示例:

s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)  
count = dm.GetWordResultCount(s)  
index = 0  
Do While index < count  
    dm\_ret
= dm.GetWordResultPos(s,index,intX,intY)  
    word = dm.GetWordResultStr(s,index)  
    MessageBox
intX&","&intY&","&word  
    index = index + 1   
Loop