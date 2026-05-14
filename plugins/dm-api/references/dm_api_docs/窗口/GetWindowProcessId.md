# GetWindowProcessId

**分类:** 窗口

**签名:** `long GetWindowProcessId(hwnd)`

**描述:** 获取指定窗口所在的进程ID.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |

## 返回值

- 返回整型表示的是进程ID

## 示例

```vbs
process_id =
dm.GetWindowProcessId(hwnd)
```
