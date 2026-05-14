# WriteDataAddrFromBin

**分类:** 内存

**签名:** `long WriteDataAddrFromBin(hwnd,addr,data,len)`

**描述:** 对指定地址写入二进制数据,只不过直接从数据指针获取数据写入,不通过字符串. 适合高级用户.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| data | int | 数据指针 |
| len | int | 数据长度 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.WriteDataAddrFromBin(hwnd,2934793257239,1231234,10)
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
