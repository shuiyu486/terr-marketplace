函数简介:

截取指定图片中的图像,并返回此句柄.

函数原型:  
  
long FaqCaptureFromFile(x1, y1, x2, y2, file, quality)

参数定义:  
  
x1 整形数: 左上角X坐标

y1 整形数: 左上角Y坐标

x2 整形数: 右下角X坐标

y2 整形数: 右下角Y坐标

file 字符串: 图片文件名,图像格式基本都支持.

quality 整形数: 图像或动画品质,或者叫压缩率,此值越大图像质量越好 取值范围（1-100或者250）.当此值为250时,会截取无损bmp图像数据.

返回值:

整形数:  
图像或者动画句柄

示例:

handle =
dm.FaqCaptureFromFile(0,0,2000,2000,"c:\test.bmp",50)

注:如果上一次的FaqPost还没有处理完毕,那么此函数调用会失败,要释放上一次的FaqPost,请调用FaqCancel函数