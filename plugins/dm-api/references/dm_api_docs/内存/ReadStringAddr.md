# ReadStringAddr

**分类:** 内存

**签名:** `string ReadStringAddr(hwnd,addr,type,len)`

**描述:** 读取指定地址的字符串，可以是GBK字符串或者是Unicode字符串.(必须事先知道内存区的字符串编码方式)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| type | int | 字符串类型,取值如下 |
| GBK | str |  |
| Unicode | str |  |
| UTF8 | str |  |
| len | int | 需要读取的字节数目.如果为0，则自动判定字符串长度. |

## 返回值

- 读取到的字符串 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadStringAddr(hwnd,123456 ,0,0)
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
