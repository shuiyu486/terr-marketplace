# FindStrFast

**分类:** 文字识别

**签名:** `long FindStrFast(x1,y1,x2,y2,string,color_format,sim,intX,intY)`

**描述:** 同FindStr。

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| string | str | 待查找的字符串,可以是字符串组合，比如"长安|洛阳|大雁塔",中间用"|"来分割字符串 |
| color_format | str | 颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例.注意，RGB和HSV,以及灰度格式都支持. |
| sim | double | 相似度,取值范围0.1-1.0 |
| intX | int* | 返回X坐标 没找到返回-1 |
| intY | int* | 返回Y坐标 没找到返回-1 |

## 返回值

- 返回字符串的索引 没找到返回-1, 比如"长安|洛阳",若找到长安，则返回0

## 示例

```vbs
dm_ret = dm.FindStrFast(0,0,2000,2000,"长安","9f2e3f-000000",1.0,intX,intY)
If intX >= 0 and intY
>= 0 Then
dm.MoveTo intX,intY
End If

dm_ret = dm.FindStrFast(0,0,2000,2000,"长安|洛阳","9f2e3f-000000",0.9,intX,intY)
If intX >= 0 and intY
>= 0 Then
dm.MoveTo intX,intY
End If

// 查找时,对多行文本进行换行,换行分隔符是"|". 语法是在","后增加换行字符串.任意字符串都可以.
dm_ret = dm.FindStrFast(0,0,2000,2000,"长安|洛阳","9f2e3f-000000,|",0.9,intX,intY)
If intX >= 0 and intY
>= 0 Then
dm.MoveTo intX,intY
End If
```

## 注意

- 此函数比FindStr要快很多，尤其是在字库很大时，或者模糊识别时，效果非常明显。
- 推荐使用此函数。
- 另外由于此函数是只识别待查找的字符，所以可能会有如下情况出现问题。
- 比如 字库中有"张和三" 一共3个字符数据，然后待识别区域里是"张和三",如果用FindStr查找
- "张三"肯定是找不到的，但是用FindStrFast却可以找到，因为"和"这个字符没有列入查找计划中
- 所以，在使用此函数时，也要特别注意这一点。
