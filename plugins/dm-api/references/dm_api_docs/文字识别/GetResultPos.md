函数简介:

对插件部分接口的返回值进行解析,并根据指定的第index个坐标,返回具体的值

函数原型:  
  
long GetResultPos(ret,index,intX,intY)

参数定义:  
  
ret 字符串:部分接口的返回串  
index 整形数: 第几个坐标  
intX 变参指针: 返回X坐标  
intY 变参指针: 返回Y坐标

返回值:

整形数:  
0:失败  
1:成功

示例:

s =
dm.FindColorEx(0,0,2000,2000,"123456-000000|abcdef-202020",1.0,0)  
count = dm.GetResultCount(s)  
index = 0  
Do While index < count  
    dm\_ret =
dm.GetResultPos(s,index,intX,intY)  
    MessageBox
intX&","&intY   
    index = index + 1   
Loop