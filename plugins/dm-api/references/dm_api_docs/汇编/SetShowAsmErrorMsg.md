# SetShowAsmErrorMsg

**分类:** 汇编

**签名:** `long SetShowAsmErrorMsg(show)`

**描述:** 设置是否弹出汇编功能中的错误提示,默认是打开.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| show | int | 0表示不打开,1表示打开 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.SetShowAsmErrorMsg(0)
```
