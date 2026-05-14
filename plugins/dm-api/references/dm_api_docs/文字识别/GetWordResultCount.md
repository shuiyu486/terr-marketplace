# GetWordResultCount

**分类:** 文字识别

**签名:** `long GetWordResultCount(str)`

**描述:** 在使用GetWords进行词组识别以后,可以用此接口进行识别词组数量的计算.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| str | str | GetWords接口调用以后的返回值 |

## 返回值

- 返回词组数量

## 示例

```vbs
s = dm.GetWords(0,0,2000,2000,"000000-000000",1.0)
count = dm.GetWordResultCount(s)
MessageBox count
```
