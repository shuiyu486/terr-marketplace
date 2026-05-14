# UseDict

**分类:** 文字识别

**签名:** `long UseDict(index)`

**描述:** 表示使用哪个字库文件进行识别(index范围:0-99)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | 字库编号(0-99) |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm_ret = dm.UseDict(1)
ss = dm.Ocr(0,0,2000,2000,"FFFFFF-000000",1.0)
dm_ret = dm.UseDict(0)
```
