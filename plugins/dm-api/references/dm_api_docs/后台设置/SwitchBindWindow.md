# SwitchBindWindow

**分类:** 后台设置

**签名:** `long SwitchBindWindow(hwnd)`

**描述:** 在不解绑的情况下,切换绑定窗口.(必须是同进程窗口)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 需要切换过去的窗口句柄 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
// 绑定为后台
dm_ret = dm.BindWindow(hwnd,"dx","dx","dx",101)
// 切换
hwnd1 = 111
dm.SwitchBindWindow(hwnd1)
```

## 注意

- 此函数一般用在绑定以后，窗口句柄改变了的情况。如果必须不解绑，那么此函数就很有用了。
