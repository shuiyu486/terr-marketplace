函数简介:

高级用户使用,在不使用字库进行词组识别前,可设定文字的行距,默认行距是1

函数原型:  
  
long SetRowGapNoDict(row\_gap)

参数定义:  
  
row\_gap 整形数:文字行距

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.SetRowGapNoDict(3)