# ReadIntAddr

**分类:** 内存

**签名:** `LONGLONG ReadIntAddr(hwnd,addr,type)`

**描述:** 读取指定地址的整数数值，类型可以是8位，16位 32位 或者64位

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| type | int | 整数类型,取值如下 |

## 返回值

- 读取到的数值 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadIntAddr(hwnd,123456
,0)
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
