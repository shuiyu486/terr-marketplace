函数简介:

释放指定的图片,此函数不必要调用,除非你想节省内存.

函数原型:  
  
long FreePic(pic\_name)

参数定义:  
  
pic\_name 字符串: 文件名
比如"1.bmp|2.bmp|3.bmp" 等,可以使用通配符,比如

         
"\*.bmp" 这个对应了所有的bmp文件

         
"a?c\*.bmp" 这个代表了所有第一个字母是a 第三个字母是c 第二个字母任意的所有bmp文件

         
"abc???.bmp|1.bmp|aa??.bmp" 可以这样任意组合.

返回值:

整形数:  
0:失败  
1:成功

示例:

PutAttachment "c:\test","\*.bmp"  
dm\_ret = dm.SetPath("c:\test")

all\_pic =
"1.bmp|2.bmp|3.bmp"  
dm\_ret = dm.LoadPic(all\_pic)

dm\_ret = dm.FreePic(all\_pic)