# AppendPicAddr

**分类:** 图色

**签名:** `string AppendPicAddr(pic_info,addr,size)`

**描述:** 对指定的数据地址和长度，组合成新的参数.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pic_info | str | 老的地址描述串 |
| addr | int | 数据地址 |
| size | int | 数据长度 |

## 返回值

- 新的地址描述串

## 示例

```vbs
pic_info = ""
pic_info = dm.AppendPicAddr(pic_info,12034,643)
pic_info = dm.AppendPicAddr(pic_info,328435,8935)
pic_info = dm.AppendPicAddr(pic_info,809234,789)
```
