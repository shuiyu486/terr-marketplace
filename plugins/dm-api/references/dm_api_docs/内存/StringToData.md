# StringToData

**分类:** 内存

**签名:** `string StringToData(value,type)`

**描述:** 把字符串转换成二进制形式.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| value | str | 需要转化的字符串 |
| type | int | 取值如下: |
| Ascii表达的 | str |  |
| Unicode表达的 | str |  |
| UTF8表达的 | str |  |

## 返回值

- 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

## 示例

```vbs
string_data =  dm.StringToData("12345678",1)
dm_ret = dm.FindData(hwnd,"00000000-7fffffff",string_data)
```
