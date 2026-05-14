函数简介:

当执行FindPicXXX系列接口时,当触发多线程查找条件时,设置开启的最大线程数量. 注意,不可以超过当前CPU核心数.

函数原型:  
  
long SetFindPicMultithreadLimit(limit)

参数定义:

limit 整形数: 最大线程数,不能超过当前CPU核心数. 超过无效. 0表示无限制.

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

dm.SetFindPicMultithreadLimie 2  
dm.FindPicXXX