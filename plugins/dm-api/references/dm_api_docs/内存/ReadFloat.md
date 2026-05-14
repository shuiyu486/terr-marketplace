# ReadFloat

**分类:** 内存

**签名:** `float ReadFloat(hwnd,addr)`

**描述:** 读取指定地址的单精度浮点数

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr | str | 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。+表示地址加，-表示地址减 模块名必须用<>符号来圈起来 例如: |

## 返回值

- 单精度浮点数: 读取到的数值 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadFloat(hwnd,"4DA678")
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
