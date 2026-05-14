# TerminateProcess

**分类:** 内存

**签名:** `long TerminateProcess(pid)`

**描述:** 根据指定的PID，强制结束进程.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程ID. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
hwnd = dm.GetMousePointWindow()
pid = dm.GetWindowProcessId(hwnd)
dm.TerminateProcess pid
```

## 注意

- 另外DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
