# GetWindowThreadId

**分类:** 窗口

**签名:** `long GetWindowThreadId(hwnd)`

**描述:** 获取指定窗口所在的线程ID.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |

## 返回值

- 返回整型表示的是线程ID

## 示例

```vbs
thread_id = dm.GetWindowThreadId(hwnd)
```
