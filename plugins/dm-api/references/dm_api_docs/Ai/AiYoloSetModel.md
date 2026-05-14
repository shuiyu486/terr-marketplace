函数简介:

需要先加载Ai模块. 从文件加载指定的模型.

函数原型:  
  
long AiYoloSetModel(index,file,pwd)

参数定义:

index 整形数**:** 模型的序号. 最多支持20个. 从0开始

file字符串**:** 模型文件名. 比如"xxxx.onnx"或者"xxxx.dmx"

pwd字符串**:** 模型的密码. 仅对dmx格式有效.

返回值:

整形数:  
1  表示成功  
0  失败

示例:

dm.AiYoloSetModel 0,"xxxx.onnx",""  
dm.AiYoloSetModel 1,"xxxx.dmx","123"

注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型. 另外,加载onnx时得确保和这个onnx同名的class文件也在同目录下.   
比如加载xxxx.onnx,那么必须得有个相应的xxxx.class.