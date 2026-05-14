# AiYoloFreeModel

**分类:** Ai

**签名:** `long AiYoloFreeModel(index)`

**描述:** 需要先加载Ai模块. 卸载指定的模型

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | **:** 模型的序号. 最多支持20个. 从0开始 |

## 返回值

- 1  表示成功
- 0  失败

## 示例

```vbs
dm.AiYoloFreeModel 0
dm.AiYoloFreeModel 1
```

## 注意

- 模型内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.
