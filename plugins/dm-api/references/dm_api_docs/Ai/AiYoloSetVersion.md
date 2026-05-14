# AiYoloSetVersion

**分类:** Ai

**签名:** `long AiYoloSetVersion(ver)`

**描述:** 需要先加载Ai模块. 设置Yolo的版本

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| ver | str | **:** Yolo的版本信息. 需要在加载Ai模块后,第一时间调用. 目前可选的值只有"v5-7.0" |

## 返回值

- 1  表示成功
- 0  失败

## 示例

```vbs
dm.AiYoloSetVersion "v5-7.0"
```
