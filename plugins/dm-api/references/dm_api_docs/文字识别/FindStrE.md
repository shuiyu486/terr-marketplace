函数简介:

在屏幕范围(x1,y1,x2,y2)内,查找string(可以是任意个字符串的组合),并返回符合color\_format的坐标位置,相似度sim同Ocr接口描述.

(多色,差色查找类似于Ocr接口,不再重述)

易语言用不了FindStr可以用此接口来代替

函数原型:  
  
string FindStrE(x1,y1,x2,y2,string,color\_format,sim)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
string 字符串:待查找的字符串, 可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串  
color\_format 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例.注意，RGB和HSV,以及灰度格式都支持.  
sim 双精度浮点数:相似度,取值范围0.1-1.0

返回值:

字符串:  
返回字符串序号以及X和Y坐标,形式如"id|x|y", 比如"0|100|200",没找到时，id和X以及Y均为-1，"-1|-1|-1"

示例:

pos = dm.FindStrE(0,0,2000,2000,"长安","9f2e3f-000000",1.0)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

pos = dm.FindStrE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",1.0)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

// 查找时,对多行文本进行换行,换行分隔符是"|". 语法是在","后增加换行字符串.任意字符串都可以.  
pos = dm.FindStrE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000,|",1.0)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

注: 此函数的原理是先Ocr识别，然后再查找。所以速度比FindStrFastE要慢，尤其是在字库  
很大，或者模糊度不为1.0时。

一般字库字符数量小于100左右，模糊度为1.0时，用FindStrE要快一些,否则用FindStrFastE.