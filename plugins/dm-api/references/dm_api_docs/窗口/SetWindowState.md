# SetWindowState

**分类:** 窗口

**签名:** `long SetWindowState(hwnd,flag)`

**描述:** 设置窗口的状态

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| flag | int | 取值定义如下 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.SetWindowState(hwnd,0)
```
