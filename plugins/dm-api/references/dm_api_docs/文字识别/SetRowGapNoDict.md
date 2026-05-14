# SetRowGapNoDict

**分类:** 文字识别

**签名:** `long SetRowGapNoDict(row_gap)`

**描述:** 高级用户使用,在不使用字库进行词组识别前,可设定文字的行距,默认行距是1

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| row_gap | int | 文字行距 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.SetRowGapNoDict(3)
```
