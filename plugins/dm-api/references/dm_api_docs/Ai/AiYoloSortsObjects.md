函数简介:

需要先加载Ai模块. 把通过AiYoloDetectObjects的结果进行排序. 排序按照从上到下,从左到右.

函数原型:  
  
string AiYoloSortsObjects(objects,height)

参数定义:

objects 字符串:
AiYoloDetectObjects的返回值

height整形数: 行高信息. 排序时需要使用此行高. 用于确定两个检测框是否处于同一行. 如果两个框的Y坐标相差绝对值小于此行高,认为是同一行.

返回值:

字符串:  
返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....".
如果没检测到任何对象,返回空字符串.

示例:

dm.AiYoloUseModel 0  
objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)  
sorted\_objects = dm.AiYoloSortsObjects(objects)