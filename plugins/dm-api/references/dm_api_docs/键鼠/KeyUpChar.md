# KeyUpChar

**分类:** 键鼠

**签名:** `long KeyUpChar(key_str)`

**描述:** 弹起来虚拟键key_str

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| key_str | str | **:** 字符串描述的键码. 大小写无所谓**. [点这里查看具体对应关系](键码对应表.htm).** |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.KeyUpChar "enter"
dm.KeyUpChar "1"
dm.KeyUpChar "F1"
dm.KeyUpChar "a"
dm.KeyUpChar "B"
```
