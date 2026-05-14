# ReadDoubleAddr

**分类:** 内存

**签名:** `double ReadDoubleAddr(hwnd,addr)`

**描述:** 读取指定地址的双精度浮点数

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |

## 返回值

- 读取到的数值 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadDoubleAddr(hwnd,123456)
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
