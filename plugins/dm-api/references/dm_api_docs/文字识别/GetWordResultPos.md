# GetWordResultPos

**分类:** 文字识别

**签名:** `long GetWordResultPos(str,index,intX,intY)`

**描述:** 在使用GetWords进行词组识别以后,可以用此接口进行识别各个词组的坐标

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| str | str | GetWords的返回值 |
| index | int | 表示第几个词组 |
| intX | int* | 返回的X坐标 |
| intY | int* | 返回的Y坐标 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)
count = dm.GetWordResultCount(s)
index = 0
Do While index < count
dm_ret = dm.GetWordResultPos(s,index,intX,intY)
MessageBox
intX&","&intY
index = index + 1
Loop
```
