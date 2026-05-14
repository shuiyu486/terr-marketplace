# WriteInt

**分类:** 内存

**签名:** `long WriteInt(hwnd,addr,type,v)`

**描述:** 对指定地址写入整数数值，类型可以是8位，16位 32位 或者64位

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr | str | 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。+表示地址加，-表示地址减 模块名必须用<>符号来圈起来 例如: |
| type | int | 整数类型,取值如下 |
| v | long | 整形数值 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.WriteInt(hwnd,"4DA678",0,100)
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
