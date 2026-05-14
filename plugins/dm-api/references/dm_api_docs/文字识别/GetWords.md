# GetWords

**分类:** 文字识别

**签名:** `string GetWords(x1, y1, x2, y2, color, sim)`

**描述:** 根据指定的范围,以及设定好的词组识别参数(一般不用更改,除非你真的理解了)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 左上角X坐标 |
| y1 | int | 左上角Y坐标 |
| x2 | int | 右下角X坐标 |
| y2 | int | 右下角Y坐标 |
| color | str | 颜色格式串.注意，RGB和HSV,以及灰度格式都支持. |
| sim | double | 相似度 0.1-1.0 |

## 返回值

- 识别到的格式串,要用到专用函数来解析

## 示例

```vbs
s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)
count = dm.GetWordResultCount(s)
index = 0
Do While index < count
dm_ret
= dm.GetWordResultPos(s,index,intX,intY)
word = dm.GetWordResultStr(s,index)
MessageBox
intX&","&intY&","&word
index = index + 1
Loop
```
