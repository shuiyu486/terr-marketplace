# SetWordLineHeight

**分类:** 文字识别

**签名:** `long SetWordLineHeight(line_height)`

**描述:** 高级用户使用,在识别词组前,可设定文字的平均行高,默认的词组行高是10

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| line_height | int | 行高 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.SetWordLineHeight(15)
```
