# SetWindowText

**分类:** 窗口

**签名:** `long SetWindowText(hwnd,title)`

**描述:** 设置窗口的标题

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| titie | str | 标题 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.SetWindowText(hwnd,"test")
```
