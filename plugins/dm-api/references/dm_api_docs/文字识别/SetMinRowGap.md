# SetMinRowGap

**分类:** 文字识别

**签名:** `long SetMinRowGap(min_row_gap)`

**描述:** 高级用户使用,在识别前,如果待识别区域有多行文字,可以设定行间距,默认的行间距是1,

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| min_row_gap | int | 最小行间距 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.SetMinRowGap(2)
```
