# EnableIme

**分类:** 后台设置

**签名:** `long EnableIme(enable)`

**描述:** 设置是否关闭绑定窗口所在进程的输入法.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 1 开启 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
// 绑定为后台
dm_ret = dm.BindWindow(hwnd,"dx","dx","dx",101)
…
// 关闭输入法
dm.EnableIme 0

…
// 再开启输入法
dm.EnableIme 1
```

## 注意

- 此函数必须在绑定后调用才有效果.
