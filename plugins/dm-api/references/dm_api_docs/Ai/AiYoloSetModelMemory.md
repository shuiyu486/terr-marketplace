函数简介:

需要先加载Ai模块. 从内存加载指定的模型. 仅支持dmx格式的内存

函数原型:  
  
long AiYoloSetModelMemory(index,data,size,pwd)

参数定义:

index 整形数**:** 模型的序号. 最多支持20个. 从0开始

data 整形数**:** dmx模型的内存地址

size 整形数**:** dmx模型的大小

pwd字符串**:** dmx模型的密码

返回值:

整形数:  
1  表示成功  
0  失败

示例:

dm.AiYoloSetModelMemory 0,2343253,23432432,"123"

注:模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.