# AiYoloSetModelMemory

**分类:** Ai

**签名:** `long AiYoloSetModelMemory(index,data,size,pwd)`

**描述:** 需要先加载Ai模块. 从内存加载指定的模型. 仅支持dmx格式的内存

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | **:** 模型的序号. 最多支持20个. 从0开始 |
| data | int | **:** dmx模型的内存地址 |
| size | int | **:** dmx模型的大小 |
| pwd | str | **:** dmx模型的密码 |

## 返回值

- 1  表示成功
- 0  失败

## 示例

```vbs
dm.AiYoloSetModelMemory 0,2343253,23432432,"123"
```

## 注意

- 模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.
