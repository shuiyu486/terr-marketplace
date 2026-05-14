函数简介:

查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

这个函数可以查找多个图片,并且返回所有找到的图像的坐标. 这个函数要求图片是数据地址.

函数原型:  
  
string FindPicMemEx(x1, y1, x2, y2, pic\_info, delta\_color,sim, dir)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
pic\_info 字符串: 图片数据地址集合. 格式为"地址1,长度1|地址2,长度2.....|地址n,长度n". 可以用[AppendPicAddr](AppendPicAddr.htm)来组合.   
         
地址表示24位位图资源在内存中的首地址，用十进制的数值表示  
         
长度表示位图资源在内存中的长度，用十进制数值表示.  
delta\_color 字符串:颜色色偏
比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示)
. 如果这里的色偏是2位，表示使用灰度找图. 比如"20"  
sim 双精度浮点数:相似度,取值范围0.1-1.0  
dir 整形数:查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上

返回值:

字符串:  
返回的是所有找到的坐标格式如下:"id,x,y|id,x,y..|id,x,y"
(图片左上角的坐标)

比如"0,100,20|2,30,40"
表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),第二个是序号为2的图片,坐标(30,40)  
(由于内存限制,返回的图片数量最多为1500个左右)

示例:

pic\_info = ""  
pic\_info = dm.AppendPicAddr(pic\_info,12034,643)  
pic\_info = dm.AppendPicAddr(pic\_info,328435,8935)  
pic\_info = dm.AppendPicAddr(pic\_info,809234,789)  
dm\_ret = dm.FindPicMemEx(0,0,2000,2000, pic\_info,"020202",1.0,0)  
If len(dm\_ret) > 0 Then  
   ss =
split(dm\_ret,"|")  
   index = 0  
   count = UBound(ss) + 1  
   Do While index < count  
      TracePrint
ss(index)  
      sss =
split(ss(index),",")  
      id =
int(sss(0))  
      x =
int(sss(1))  
      y =
int(sss(2))  
      dm.MoveTo
x,y  
      Delay 1000  
      index =
index+1  
   Loop  
End If

注 : 内存中的图片格式必须是24位色，并且不能加密.