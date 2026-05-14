函数简介:

根据部分Ex接口的返回值，然后在所有坐标里找出距离指定坐标最近的那个坐标.

函数原型:  
  
string FindNearestPos(all\_pos,type,x,y)

参数定义:  
  
all\_pos 字符串: 坐标描述串。  一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx,
FindMultiColorEx,和FindPicEx的返回值.  
type 整形数:  取值为0或者1

     如果all\_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0

     如果all\_pos的内容是由FindColorEx,
FindMultiColorEx,FindColorBlockEx返回，那么取值为1

如果all\_pos的内容是由OcrEx返回，那么取值为2

     如果all\_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3

x 整形数: 横坐标  
y 整形数: 纵坐标

返回值:  
  
字符串:  
返回的格式和type有关，如果type为0，那么返回的格式是"id,x,y"

如果type为1,那么返回的格式是"x,y".

示例:

ret =
dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)  
ret = dm.FindNearestPos(ret,1,100,100)  
TracePrint ret

ret =
dm.FindPicEx(0,0,2000,2000,"a.bmp","000000",1.0,0)  
ret = dm.FindNearestPos(ret,0,100,100)  
TracePrint ret

ret = dm.OcrEx(0,0,2000,2000,"ffffff",1.0)  
ret = dm.FindNearestPos(ret,2,100,100)  
TracePrint ret

ret = dm.FindPicExS(0,0,2000,2000,"test.bmp|test2.bmp","020202",1.0,0)
  
ret = dm.FindNearestPos(ret,3,100,100)  
TracePrint ret