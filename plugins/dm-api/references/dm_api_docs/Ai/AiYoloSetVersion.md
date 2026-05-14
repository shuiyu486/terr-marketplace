函数简介:

需要先加载Ai模块. 设置Yolo的版本

函数原型:  
  
long AiYoloSetVersion(ver)

参数定义:

ver字符串**:** Yolo的版本信息. 需要在加载Ai模块后,第一时间调用. 目前可选的值只有"v5-7.0"

返回值:

整形数:  
1  表示成功  
0  失败

示例:

dm.AiYoloSetVersion "v5-7.0"