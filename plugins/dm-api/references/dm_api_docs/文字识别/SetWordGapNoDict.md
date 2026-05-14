函数简介:

高级用户使用,在不使用字库进行词组识别前,可设定词组间的间隔,默认的词组间隔是5

函数原型:  
  
long SetWordGapNoDict(word\_gap)

参数定义:  
  
word\_gap 整形数:单词间距

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.SetWordGapNoDict(1)