函数简介:

高级用户使用,在不使用字库进行词组识别前,可设定文字的列距,默认列距是1

函数原型:  
  
long SetColGapNoDict(col\_gap)

参数定义:  
  
col\_gap 整形数:文字列距

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.SetColGapNoDict(3)