# GetWordsNoDict

**分类:** 文字识别

**签名:** `string GetWordsNoDict(x1, y1, x2, y2, color)`

**描述:** 根据指定的范围,以及设定好的词组识别参数(一般不用更改,除非你真的理解了)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 左上角X坐标 |
| y1 | int | 左上角Y坐标 |
| x2 | int | 右下角X坐标 |
| y2 | int | 右下角Y坐标 |
| color | str | 颜色格式串.注意，RGB和HSV,以及灰度格式都支持. |

## 返回值

- 识别到的格式串,要用到专用函数来解析

## 示例

```vbs
s = dm.GetWordsNoDict(0,0,2000,2000,"000000-000000")
count = dm.GetResultCount(s)
index = 0
Do While index < count
dm_ret
= dm.GetResultPos(s,index,intX,intY)
MessageBox
intX&","&intY
index = index + 1
Loop
```
