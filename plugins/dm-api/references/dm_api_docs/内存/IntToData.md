# IntToData

**分类:** 内存

**签名:** `string IntToData(value,type)`

**描述:** 把整数转换成二进制形式.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| value | long | 需要转化的整型数 |
| type | int | 取值如下: |

## 返回值

- 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

## 示例

```vbs
int_data =  dm.IntToData(&H12345678,0)
dm_ret = dm.FindData(hwnd,"00000000-7fffffff",int_data)
```
