函数简介:

需要先加载Ai模块. 把通过AiYoloDetectObjects或者是AiYoloSortsObjects的结果,按照顺序把class信息连接输出.

函数原型:  
  
string AiYoloObjectsToString(objects)

参数定义:

objects 字符串:
AiYoloDetectObjects或者AiYoloSortsObjects的返回值.

返回值:

字符串:  
返回的是class信息连接后的信息.

示例:

dm.AiYoloUseModel 0  
objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)  
sorted\_objects = dm.AiYoloSortsObjects(objects)  
TracePrint dm.AiYoloObjectsToString(sorted\_objects)