# KeyDownChar

**分类:** 键鼠

**签名:** `long KeyDownChar(key_str)`

**描述:** 按住指定的虚拟键码

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| key_str | str | 字符串描述的键码. 大小写无所谓. [点这里查看具体对应关系](键码对应表.htm). |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.KeyDownChar "enter"
dm.KeyDownChar "1"
dm.KeyDownChar "F1"
dm.KeyDownChar "a"
dm.KeyDownChar "B"
```
