# EnableKeypadMsg

**分类:** 后台设置

**签名:** `long EnableKeypadMsg(enable)`

**描述:** 是否在使用dx键盘时开启windows消息.默认开启.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 禁止 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)
dm.EnableKeypadMsg 0
```

## 注意

- 此接口必须在绑定之后才能调用。
- 特殊时候使用.
