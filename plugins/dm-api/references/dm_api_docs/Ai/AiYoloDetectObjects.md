函数简介:

需要先加载Ai模块. 在指定范围内检测对象.

函数原型:  
  
string AiYoloDetectObjects(x1, y1, x2, y2,prob,iou)

参数定义:

x1 整形数:区域的左上X坐标

y1 整形数:区域的左上Y坐标

x2 整形数:区域的右下X坐标

y2 整形数:区域的右下Y坐标

prob双精度浮点数**:** 置信度,也可以认为是相似度.
超过这个prob的对象才会被检测

iou 双精度浮点数**:** 用于对多个检测框进行合并.  越大越不容易合并(很多框重叠). 越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间.   
              
可以在Yolo综合工具里进行测试.

返回值:

字符串:  
返回的是所有检测到的对象.格式是"类名,置信度,x,y,w,h|....".
如果没检测到任何对象,返回空字符串.

示例:

dm.AiYoloUseModel 0  
objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)  
if len(objects) > 0 then  
   ss = split(objects,"|")  
   index = 0  
   count = UBound(ss) + 1  
   Do While index < count  
      TracePrint
ss(index)  
      sss =
split(ss(index),",")  
      class\_info
= int(sss(0))  
      prob\_info
= Csng(sss(1))  
      x =
int(sss(2))  
      y =
int(sss(3))  
      w =
int(sss(4))  
      h = int(sss(5))  
      index =
index+1  
   Loop  
end if

注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.   
如果多个线程里,UseModel的序号是相同的,那么如果同时执行此接口时,会排队执行.