# AiYoloSetModel

**分类:** Ai

**签名:** `long AiYoloSetModel(index,file,pwd)`

**描述:** 需要先加载Ai模块. 从文件加载指定的模型.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | **:** 模型的序号. 最多支持20个. 从0开始 |
| file | str | **:** 模型文件名. 比如"xxxx.onnx"或者"xxxx.dmx" |
| pwd | str | **:** 模型的密码. 仅对dmx格式有效. |

## 返回值

- 1  表示成功
- 0  失败

## 示例

```vbs
dm.AiYoloSetModel 0,"xxxx.onnx",""
dm.AiYoloSetModel 1,"xxxx.dmx","123"
```

## 注意

- 模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 另外,加载onnx时得确保和这个onnx同名的class文件也在同目录下.
- 比如加载xxxx.onnx,那么必须得有个相应的xxxx.class.
