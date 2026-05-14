# GetWindow

**分类:** 窗口

**签名:** `long GetWindow(hwnd,flag)`

**描述:** 获取给定窗口相关的窗口句柄

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |
| flag | int | 取值定义如下 |

## 返回值

- 返回整型表示的窗口句柄

## 示例

```vbs
own_hwnd = dm.GetWindow(hwnd,6)
```
