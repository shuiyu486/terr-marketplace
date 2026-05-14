# WriteStringAddr

**分类:** 内存

**签名:** `long WriteStringAddr(hwnd,addr,type,v)`

**描述:** 对指定地址写入字符串，可以是Ascii字符串或者是Unicode字符串

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| type | int | 字符串类型,取值如下 |
| Ascii | str |  |
| Unicode | str |  |
| UTF8 | str |  |
| v | str | 字符串 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.WriteStringAddr(hwnd,123456 ,0,"我是来测试的")
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
