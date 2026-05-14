函数简介:

获取指定的字库中的字符数量.

函数原型:  
  
long GetDictCount(index)

参数定义:

index 整形数: 字库序号(0-99)

返回值:

整形数:  
字库数量

示例:

count = dm.GetDictCount(0)  
TracePrint "0号字库使用的字库数量是:"&count