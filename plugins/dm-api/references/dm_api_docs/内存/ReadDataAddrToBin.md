# ReadDataAddrToBin

**分类:** 内存

**签名:** `long ReadDataAddrToBin(hwnd,addr,len)`

**描述:** 读取指定地址的二进制数据,只不过返回的是内存地址,而不是字符串.适合高级用户.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr长 | int | 地址 |
| len | int | 二进制数据的长度 |

## 返回值

- 读取到的数据指针. 返回0表示读取失败. 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
value = dm.ReadDataAddrToBin(hwnd,12341234 ,10)
MessageBox  value
```

## 注意

- DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
- 需要注意的是,调用此接口获取的数据指针保存在当前对象中,到下次调用此接口时,内部就会释放.
- 哪怕是转成字节集,这个地址也还是在此字节集中使用. 如果您要此地址一直有效，那么您需要自己拷贝字节集到自己的字节集中.
