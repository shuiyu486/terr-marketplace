# GetWindowProcessPath

**分类:** 窗口

**签名:** `string GetWindowProcessPath(hwnd)`

**描述:** 获取指定窗口所在的进程的exe文件全路径.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |

## 返回值

- 返回字符串表示的是exe全路径名

## 示例

```vbs
process_path =
dm.GetWindowProcessPath(hwnd)
```
