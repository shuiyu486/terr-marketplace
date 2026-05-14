# FindStrE

**分类:** 文字识别

**签名:** `string FindStrE(x1,y1,x2,y2,string,color_format,sim)`

**描述:** 在屏幕范围(x1,y1,x2,y2)内,查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置,相似度sim同Ocr接口描述.

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

- 返回字符串序号以及X和Y坐标,形式如"id|x|y", 比如"0|100|200",没找到时，id和X以及Y均为-1，"-1|-1|-1"

## 示例

```vbs
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
```

## 注意

- 此函数的原理是先Ocr识别，然后再查找。所以速度比FindStrFastE要慢，尤其是在字库
- 很大，或者模糊度不为1.0时。
- 一般字库字符数量小于100左右，模糊度为1.0时，用FindStrE要快一些,否则用FindStrFastE.
