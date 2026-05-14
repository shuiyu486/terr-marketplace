# SetColGapNoDict

**分类:** 文字识别

**签名:** `long SetColGapNoDict(col_gap)`

**描述:** 高级用户使用,在不使用字库进行词组识别前,可设定文字的列距,默认列距是1

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| col_gap | int | 文字列距 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.SetColGapNoDict(3)
```
