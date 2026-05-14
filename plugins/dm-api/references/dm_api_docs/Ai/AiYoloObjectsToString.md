# AiYoloObjectsToString

**分类:** Ai

**签名:** `string AiYoloObjectsToString(objects)`

**描述:** 需要先加载Ai模块. 把通过AiYoloDetectObjects或者是AiYoloSortsObjects的结果,按照顺序把class信息连接输出.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| objects | str | AiYoloDetectObjects或者AiYoloSortsObjects的返回值. |

## 返回值

- 返回的是class信息连接后的信息.

## 示例

```vbs
dm.AiYoloUseModel 0
objects = dm.AiYoloDetectObjects(0,0,2000,2000,0.5,0.45)
sorted_objects = dm.AiYoloSortsObjects(objects)
TracePrint dm.AiYoloObjectsToString(sorted_objects)
```
