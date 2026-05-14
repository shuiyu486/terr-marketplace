# OpenProcess

**分类:** 内存

**签名:** `long OpenProcess(pid)`

**描述:** 根据指定pid打开进程，并返回进程句柄.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程pid |

## 返回值

- 进程句柄, 可用于进程相关操作(读写操作等),记得操作完成以后，自己调用CloseHandle关闭句柄.

## 示例

```vbs
hwnd = dm.GetMousePointWindow()
pid = dm.GetWindowProcessId(hwnd)
handle = dm.OpenProcess(pid)
……
CloseHandle(handle) // 这里自己定义导入函数
```
