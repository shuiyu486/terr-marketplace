# GetModuleSize

**分类:** 内存

**签名:** `long GetModuleSize(hwnd,module)`

**描述:** 根据指定的窗口句柄，来获取对应窗口句柄进程下的指定模块的大小

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| module | str | 模块名 |

## 返回值

- 模块的大小

## 示例

```vbs
module_size = dm.GetModuleSize(hwnd,"gdi32.dll")
MessageBox  module_size
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
