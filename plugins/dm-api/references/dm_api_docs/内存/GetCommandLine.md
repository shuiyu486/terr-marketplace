# GetCommandLine

**分类:** 内存

**签名:** `string GetCommandLine(hwnd)`

**描述:** 获取指定窗口所在进程的启动命令行

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |

## 返回值

- 读取到的启动命令行

## 示例

```vbs
command = dm.GetCommandLine(hwnd)
MessageBox  command
```
