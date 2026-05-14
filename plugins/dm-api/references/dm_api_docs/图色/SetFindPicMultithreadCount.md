函数简介:

当执行FindPicXXX系列接口时,当图片个数少于count时,使用单线程查找,否则使用多线程。 这个count默认是4.

函数原型:  
  
long SetFindPicMultithreadCount(count)

参数定义:

count 整形数: 图片数量. 最小不能小于2. 因为1个图片必定是单线程. 这个值默认是4.如果你不更改的话.

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

dm.SetFindPicMultithreadCount 2  
dm.FindPicXXX

注 : 这个只是设置多线程查找的一个条件.另外一个开关是[EnableFindPicMultithread](EnableFindPicMultithread.htm).