# WriteData

**分类:** 内存

**签名:** `long WriteData(hwnd,addr,data)`

**描述:** 对指定地址写入二进制数据

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr | str | 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。+表示地址加，-表示地址减 模块名必须用<>符号来圈起来 例如: |
| data | str | 二进制数据，以字符串形式描述，比如"12 34 56 78 90 ab cd" |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.WriteData(hwnd,"4DA678","12 34 56 78 90 ab cd")
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
