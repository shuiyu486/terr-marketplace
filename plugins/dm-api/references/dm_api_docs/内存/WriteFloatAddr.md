# WriteFloatAddr

**分类:** 内存

**签名:** `long WriteFloatAddr(hwnd,addr,v)`

**描述:** 对指定地址写入单精度浮点数

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| v | float | 单精度浮点数 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.WriteFloatAddr(hwnd,123456 ,2.34)
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
