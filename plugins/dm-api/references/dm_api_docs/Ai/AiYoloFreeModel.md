函数简介:

需要先加载Ai模块. 卸载指定的模型

函数原型:  
  
long AiYoloFreeModel(index)

参数定义:

index 整形数**:** 模型的序号. 最多支持20个. 从0开始

返回值:

整形数:  
1  表示成功  
0  失败

示例:

dm.AiYoloFreeModel 0  
dm.AiYoloFreeModel 1

注:模型内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.