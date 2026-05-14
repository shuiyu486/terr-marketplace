# DoubleToData

**分类:** 内存

**签名:** `string DoubleToData(value)`

**描述:** 把双精度浮点数转换成二进制形式.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| value | double | 需要转化的双精度浮点数 |

## 返回值

- 字符串形式表达的二进制数据. 可以用于WriteData FindData FindDataEx等接口.

## 示例

```vbs
double_data =  dm.DoubleToData(1.24)
dm_ret = dm.FindData(hwnd,"00000000-7fffffff",double_data)
```
