函数简介:

同FindStrE，但是不使用SetDict设置的字库，而利用系统自带的字库，速度比FindStrE稍慢

函数原型:  
  
string FindStrWithFontE(x1,y1,x2,y2,string,color\_format,sim,font\_name,font\_size,flag)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
string 字符串:待查找的字符串, 可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串  
color\_format 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度,取值范围0.1-1.0  
font\_name 字符串:系统字体名,比如"宋体"  
font\_size 整形数:系统字体尺寸，这个尺寸一定要以大漠综合工具获取的为准.如果获取尺寸看视频教程.  
flag 整形数:字体类别 取值可以是以下值的组合,比如1+2+4+8,2+4. 0表示正常字体.  
    1 : 粗体  
    2 : 斜体  
    4 : 下划线  
    8 : 删除线

返回值:

字符串:  
返回字符串序号以及X和Y坐标,形式如"id|x|y", 比如"0|100|200",没找到时，id和X以及Y均为-1，"-1|-1|-1"

示例:

pos = dm.FindStrWithFontE(0,0,2000,2000,"长安","9f2e3f-000000",1.0,"宋体",9,0)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

pos = dm.FindStrWithFontE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",1.0,"宋体",9,1+2)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

// 查找时,对多行文本进行换行,换行分隔符是"|". 语法是在","后增加换行字符串.任意字符串都可以.  
pos = dm.FindStrWithFontE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000,|",1.0,"宋体",9,1+2)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

注: 对于如何获取字体尺寸以及名字等信息，可以参考视频教程，如何使用系统字库.