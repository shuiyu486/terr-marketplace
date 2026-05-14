# SetWordGapNoDict

**分类:** 文字识别

**签名:** `long SetWordGapNoDict(word_gap)`

**描述:** 高级用户使用,在不使用字库进行词组识别前,可设定词组间的间隔,默认的词组间隔是5

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| word_gap | int | 单词间距 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.SetWordGapNoDict(1)
```
