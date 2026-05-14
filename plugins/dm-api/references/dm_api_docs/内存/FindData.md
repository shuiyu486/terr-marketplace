# FindData

**分类:** 内存

**签名:** `string FindData(hwnd, addr_range, data)`

**描述:** 搜索指定的二进制数据,默认步长是1.默认开启多线程,默认略过Mapped的内存类型,默认是搜索可读可写可执行的内存.如果要定制搜索,请用FindDataEx

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定搜索的窗口句柄或者进程ID. 默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr_range | str | 指定搜索的地址集合，字符串类型，这个地方可以是上次FindXXX的返回地址集合,可以进行二次搜索.(类似CE的再次扫描) 如果要进行地址范围搜索，那么这个值为的形如如下(类似于CE的新搜索) "00400000-7FFFFFFF" "80000000-BFFFFFFF" "00000000-FFFFFFFF" 等. |
| data | str | 要搜索的二进制数据 以字符串的形式描述 比如"00 01 23 45 67 86 ab ce f1"等. 这里也可以支持模糊查找,用??来代替单个字节. 比如"00 01 ?? ?? 67 86 ?? ce f1"等. 注意,这里不支持半个字节,比如3?这种不行. |

## 返回值

- 返回搜索到的地址集合，地址格式如下: "addr1|addr2|addr3…|addrn" 比如"400050|423435|453430" 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

## 示例

```vbs
// 全局搜索
result = dm.FindData(hwnd,"00000000-FFFFFFFF","00 01 23 45 67 86
ab ce f1")
if len(result) = 0 then
MessageBox
"找不到"
EndScript
end if

result = split(result,"|")
count = ubound(result)+1
MessageBox "找到"&count&"个地址"

DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。
```
