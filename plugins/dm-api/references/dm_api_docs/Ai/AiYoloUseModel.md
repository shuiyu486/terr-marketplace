# AiYoloUseModel

**分类:** Ai

**签名:** `long AiYoloUseModel(index)`

**描述:** 需要先加载Ai模块. 切换当前使用的模型序号.用于AiYoloDetectXX等系列接口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | **:** 模型的序号. 最多支持20个. 从0开始 |

## 返回值

- 1  表示成功
- 0  失败

## 示例

```vbs
dm.AiYoloUseModel 0
```
