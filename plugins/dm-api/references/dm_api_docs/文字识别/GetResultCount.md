# GetResultCount

**分类:** 文字识别

**签名:** `long GetResultCount(ret)`

**描述:** 对插件部分接口的返回值进行解析,并返回ret中的坐标个数

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| ret | str | 部分接口的返回串 |

## 返回值

- 返回ret中的坐标个数

## 示例

```vbs
s =
dm.FindColorEx(0,0,2000,2000,"123456-000000|abcdef-202020",1.0,0)
count = dm.GetResultCount(s)
MessageBox count
```
