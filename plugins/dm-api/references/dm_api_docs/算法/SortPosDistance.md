函数简介:

根据部分Ex接口的返回值，然后对所有坐标根据对指定坐标的距离(或者指定X或者Y)进行从小到大的排序.

函数原型:  
  
string SortPosDistance(all\_pos,type,x,y)

参数定义:  
  
all\_pos 字符串: 坐标描述串。  一般是FindStrEx,FindStrFastEx,FindStrWithFontEx, FindColorEx, FindMultiColorEx,和FindPicEx的返回值.  
type 整形数:  取值为0或者1

     如果all\_pos的内容是由FindPicEx,FindStrEx,FindStrFastEx,FindStrWithFontEx返回，那么取值为0

     如果all\_pos的内容是由FindColorEx, FindMultiColorEx,FindColorBlockEx返回，那么取值为1

     如果all\_pos的内容是由OcrEx返回，那么取值为2

     如果all\_pos的内容是由FindPicExS,FindStrExS,FindStrFastExS返回，那么取值为3

x 整形数: 横坐标   
y 整形数: 纵坐标  
         
注意:如果x为65535并且y为0时，那么排序的结果是仅仅对x坐标进行排序,如果y为65535并且x为0时，那么排序的结果是仅仅对y坐标进行排序.

返回值:  
  
字符串:  
返回的格式和type指定的格式一致.

示例:

ret = dm.FindColorEx(0,0,2000,2000,"aaaaaa-000000",1.0,0)  
ret = dm.SortPosDistance(ret,1,100,100)  
TracePrint ret

ret = dm.FindPicEx(0,0,2000,2000,"a.bmp","000000",1.0,0)  
ret = dm.SortPosDistance(ret,0,65535,0)  
TracePrint ret

ret = dm.OcrEx(0,0,2000,2000,"ffffff",1.0)  
ret = dm.SortPosDistance(ret,2,65535,0)  
TracePrint ret

ret = dm.FindPicExS(0,0,2000,2000,"test.bmp|test2.bmp","020202",1.0,0)
  
ret = dm.SortPosDistance(ret,3,65535,0)  
TracePrint ret