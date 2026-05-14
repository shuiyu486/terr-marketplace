函数简介:

获取当前系统从开机到现在所经历过的时间，单位是毫秒

函数原型:  
  
long GetTime()

参数定义:

返回值:

整形数:  
时间(单位毫秒)

示例:

t1 = dm.GetTime()  
dm\_ret =
dm.FindPic(0,0,2000,2000,"test.bmp","000000",1.0,0,x,y)  
t2 = dm.GetTime()  
MessageBox (t2-t1)