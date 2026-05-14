# GetWordResultStr

**分类:** 文字识别

**签名:** `string GetWordResultStr(str,index)`

**描述:** 在使用GetWords进行词组识别以后,可以用此接口进行识别各个词组的内容

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| str | str | GetWords的返回值 |
| index | int | 表示第几个词组 |

## 返回值

- 返回的第index个词组内容

## 示例

```vbs
s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)
count = dm.GetWordResultCount(s)
index = 0
Do While index < count
word =
dm.GetWordResultStr(s,index)
MessageBox word
index = index + 1
Loop
```
