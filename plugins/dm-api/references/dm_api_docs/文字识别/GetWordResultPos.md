函数简介:

在使用GetWords进行词组识别以后,可以用此接口进行识别各个词组的坐标

函数原型:  
  
long GetWordResultPos(str,index,intX,intY)

参数定义:  
  
str 字符串: GetWords的返回值

index 整形数: 表示第几个词组

intX 变参指针: 返回的X坐标

intY 变参指针: 返回的Y坐标

返回值:

整形数:  
0: 失败

1: 成功

示例:

s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)  
count = dm.GetWordResultCount(s)  
index = 0  
Do While index < count  
    dm\_ret = dm.GetWordResultPos(s,index,intX,intY)  
    MessageBox
intX&","&intY   
    index = index + 1   
Loop