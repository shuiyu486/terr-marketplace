函数简介:

设置字库文件

函数原型:  
  
long SetDict(index,file)

参数定义:

index 整形数:字库的序号,取值为0-99,目前最多支持100个字库  
file 字符串:字库文件名

返回值:

整形数:  
0:失败  
1:成功

示例:

dm\_ret = dm.SetDict(0,"test.txt")  
  
注: 此函数速度很慢，全局初始化时调用一次即可，切换字库用UseDict