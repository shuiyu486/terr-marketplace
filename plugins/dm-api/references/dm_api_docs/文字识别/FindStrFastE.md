函数简介:

同FindStrE

易语言用不了FindStrFast可以用此接口来代替

函数原型:  
  
string FindStrFastE(x1,y1,x2,y2,string,color\_format,sim)

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

pos = dm.FindStrFastE(0,0,2000,2000,"长安","9f2e3f-000000",1.0)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

pos = dm.FindStrFastE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",0.9)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

// 查找时,对多行文本进行换行,换行分隔符是"|". 语法是在","后增加换行字符串.任意字符串都可以.  
pos = dm.FindStrFastE(0,0,2000,2000,"长安|洛阳","9f2e3f-000000,|",0.9)  
pos = split(pos,"|")  
If int(pos(0)) >= 0 Then  
     dm.MoveTo int(pos(1)),int(pos(2))  
End If

注: 此函数比FindStrE要快很多，尤其是在字库很大时，或者模糊识别时，效果非常明显。  
推荐使用此函数。

另外由于此函数是只识别待查找的字符，所以可能会有如下情况出现问题。

比如 字库中有"张和三" 一共3个字符数据，然后待识别区域里是"张和三",如果用FindStrE查找  
"张三"肯定是找不到的，但是用FindStrFastE却可以找到，因为"和"这个字符没有列入查找计划中  
所以，在使用此函数时，也要特别注意这一点。