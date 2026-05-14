函数简介:

转换图片格式为24位BMP格式.

函数原型:  
  
long ImageToBmp(pic\_name,bmp\_name)

参数定义:

pic\_name 字符串: 要转换的图片名  
bmp\_name 字符串: 要保存的BMP图片名

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm.ImageToBmp "1.png","1.bmp"  
dm.ImageToBmp "2.jpg","2.bmp"  
dm.ImageToBmp "3.gif","3.bmp"