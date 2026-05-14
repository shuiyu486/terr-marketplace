# ReadData

**分类:** 内存

**签名:** `string ReadData(hwnd,addr,len)`

**描述:** 读取指定地址的二进制数据

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr | str | 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。+表示地址加，-表示地址减 模块名必须用<>符号来圈起来 例如: |
| len | int | 二进制数据的长度 |

## 返回值

- 读取到的数值,以16进制表示的字符串 每个字节以空格相隔 比如"12 34 56 78 ab cd ef" 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadData(hwnd,"4DA678",10)
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
- 如果要读取的数据长度过长，比如几十K的数据，由于COM组件的限制，可能无法返回如此长的字符串. 解决办法是分批读取.
