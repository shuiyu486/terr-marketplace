函数简介:

高级用户使用,在不使用字库进行词组识别前,可设定文字的平均行高,默认的词组行高是10

函数原型:  
  
long SetWordLineHeightNoDict(line\_height)

参数定义:  
  
line\_height 整形数:行高

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.SetWordLineHeightNoDict(15)