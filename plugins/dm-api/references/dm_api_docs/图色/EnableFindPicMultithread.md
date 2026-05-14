函数简介:

当执行FindPicXXX系列接口时,是否在条件满足下(查找的图片大于等于4,这个值可以根据[SetFindPicMultithreadCount](SetFindPicMultithreadCount.htm)来修改),开启多线程查找。 默认打开.

函数原型:  
  
long EnableFindPicMultithread(enable)

参数定义:

enable 整形数: 0 关闭

        
1 打开

返回值:

整形数:  
0 : 失败  
1 : 成功

示例:

dm.EnableFindPicMultithread 0  
dm.FindPicXXX  
dm.EnableFindPicMultithread 1

注 : 如果担心开启多线程会引发占用大量CPU资源,那么可以考虑关闭此功能. 在以往版本,这个功能默认都是打开的.  
这个只是多线程查找的一个开关,另一个开关是[SetFindPicMultithreadCount](SetFindPicMultithreadCount.htm)