函数简介:

需要先加载Ai模块. 切换当前使用的模型序号.用于AiYoloDetectXX等系列接口.

函数原型:  
  
long AiYoloUseModel(index)

参数定义:

index 整形数**:** 模型的序号. 最多支持20个. 从0开始

返回值:

整形数:  
1  表示成功  
0  失败

示例:

dm.AiYoloUseModel 0