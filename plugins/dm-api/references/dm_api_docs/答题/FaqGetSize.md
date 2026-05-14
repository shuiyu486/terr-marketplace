函数简介:

获取句柄所对应的数据包的大小,单位是字节

函数原型:  
  
long FaqGetSize(handle)

参数定义:  
  
handle 整形数: 由FaqCapture返回的句柄

返回值:

整形数:  
数据包大小,一般用于判断数据大小,选择合适的压缩比率.

示例:

// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms  
handle = dm.FaqCapture(intX - 50,intY - 232,intX+272,intY-12,50,100,3000)  
packet\_size = dm.FaqGetSize(handle)  
MessageBox packet\_size