# VirtualFreeEx

**分类:** 内存

**签名:** `long VirtualFreeEx(hwnd,addr)`

**描述:** 释放用VirtualAllocEx分配的内存.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | VirtualAllocEx返回的地址 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
addr =
dm.VirtualAllocEx(hwnd,0,50,0)
dm.WriteString hwnd,cstr(hex(addr)),0,"哈哈"
dm.VirtualFreeEx hwnd,addr
```

## 注意

- 如果正常方式无法分配内存,可以尝试配合DmGuard中的memory护盾,突破部分窗口内存保护。
- 用此函数分配的内存，必须用VirtualFreeEx来释放,以免目标进程内存泄漏.
