# SetShowErrorMsg

**分类:** 基本设置

**签名:** `long SetShowErrorMsg(show)`

**描述:** 设置是否弹出错误信息,默认是打开.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| show | int | 0表示不打开,1表示打开 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.SetShowErrorMsg(0)
```
