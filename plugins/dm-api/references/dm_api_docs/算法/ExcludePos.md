函数简介:

根据部分Ex接口的返回值，排除指定范围区域内的坐标.

函数原型:  
  
string ExcludePos(all\_pos,type,x1,y1,x2,y2)

参数定义:  
  
all\_pos 字符串: 坐标描述串。  一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx,
FindMultiColorEx,和FindPicEx的返回值.  
type 整形数:  取值为0或者1

     如果all\_pos的内容是由FindPicEx,FindPicMemEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0

     如果all\_pos的内容是由FindColorEx,
FindMultiColorEx,FindColorBlockEx,FindShapeEx返回，那么取值为1

     如果all\_pos的内容是由OcrEx返回，那么取值为2

     如果all\_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3

x1 整形数: 左上角横坐标  
y1 整形数: 左上角纵坐标  
x2 整形数: 右下角横坐标  
y2 整形数: 右下角纵坐标

返回值:

字符串:  
经过筛选以后的返回值，格式和type指定的一致.

示例:

ret = dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)  
ret = dm.ExcludePos(ret,1,100,100,300,400)  
TracePrint ret

ret =
dm.FindPicEx(0,0,2000,2000,"a.bmp","000000",1.0,0)  
ret = dm.ExcludePos(ret,0,100,100,300,400)  
TracePrint ret

ret = dm.OcrEx(0,0,2000,2000,"ffffff",1.0)  
ret = dm.ExcludePos(ret,2,100,100,300,400)  
TracePrint ret

ret = dm.FindPicExS(0,0,2000,2000,"test.bmp|test2.bmp","020202",1.0,0)
  
ret = dm.ExcludePos(ret,3,100,100,300,400)  
TracePrint ret