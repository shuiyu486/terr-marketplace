函数简介:

在使用GetWords进行词组识别以后,可以用此接口进行识别各个词组的内容

函数原型:  
  
string GetWordResultStr(str,index)

参数定义:  
  
str 字符串: GetWords的返回值

index 整形数: 表示第几个词组

返回值:

字符串:  
返回的第index个词组内容

示例:

s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)  
count = dm.GetWordResultCount(s)  
index = 0  
Do While index < count  
    word =
dm.GetWordResultStr(s,index)  
    MessageBox word   
    index = index + 1   
Loop