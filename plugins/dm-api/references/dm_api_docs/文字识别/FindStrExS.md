# FindStrExS

**分类:** 文字识别

**签名:** `string FindStrExS(x1,y1,x2,y2,string,color_format,sim)`

**描述:** 在屏幕范围(x1,y1,x2,y2)内,查找string(可以是任意字符串的组合),并返回符合color_format的所有坐标位置,相似度sim同Ocr接口描述.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| string | str | 待查找的字符串, 可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串 |
| color_format | str | 颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例.注意，RGB和HSV,以及灰度格式都支持. |
| sim | double | 相似度,取值范围0.1-1.0 |

## 返回值

- 返回所有找到的坐标集合,格式如下: "str,x0,y0| str,x1,y1|......| str,xn,yn" 比如"长安,100,20|大雁塔,30,40" 表示找到了两个,第一个是长安 ,坐标是(100,20),第二个是大雁塔,坐标(30,40)

## 示例

```vbs
dm_ret = dm.FindStrExS(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",1.0)
If len(dm_ret) > 0 Then
ss
= split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
TracePrint ss(index)
sss = split(ss(index),",")
str = sss(0)
x = int(sss(1))
y = int(sss(2))
dm.MoveTo x,y
Delay 1000
index =
index+1
Loop
End If
```

## 注意

- 此函数的原理是先Ocr识别，然后再查找。所以速度比FindStrExFastS要慢，尤其是在字库
- 很大，或者模糊度不为1.0时。
- 一般字库字符数量小于100左右，模糊度为1.0时，用FindStrExS要快一些,否则用FindStrFastExS.
