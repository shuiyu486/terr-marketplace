# GetDictCount

**分类:** 文字识别

**签名:** `long GetDictCount(index)`

**描述:** 获取指定的字库中的字符数量.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | 字库序号(0-99) |

## 返回值

- 字库数量

## 示例

```vbs
count = dm.GetDictCount(0)
TracePrint "0号字库使用的字库数量是:"&count
```
