函数简介:

获取当前使用的字库序号(0-99)

函数原型:  
  
long GetNowDict()

参数定义:

返回值:

整形数:  
字库序号(0-99)

示例:

index = dm.GetNowDict()  
TracePrint "当前使用的字库序号是:"&index