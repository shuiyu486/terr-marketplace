# GetDict

**分类:** 文字识别

**签名:** `string GetDict(index,font_index)`

**描述:** 获取指定字库中指定条目的字库信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | 字库序号(0-99) |
| font_index | int | 字库条目序号(从0开始计数,数值不得超过指定字库的字库上限,具体参考[GetDictCount](GetDictCount.htm)) |

## 返回值

- 返回字库条目信息. 失败返回空串.

## 示例

```vbs
s = dm.GetDict(0,1245)
TracePrint s
s = dm.GetDict(1,678)
TracePrint s
```
