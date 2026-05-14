函数简介:

预先加载指定的图片,这样在操作任何和图片相关的函数时,将省去了加载图片的时间。调用此函数后,没必要一定要调用FreePic,插件自己会自动释放.

另外,此函数不是必须调用的,所有和图形相关的函数只要调用过一次，图片会自动加入缓存.

如果想对一个已经加入缓存的图片进行修改，那么必须先用FreePic释放此图片在缓存中占用

的内存，然后重新调用图片相关接口，就可以重新加载此图片. （当图色缓存机制打开时,具体参考[EnablePicCache](../基本设置/EnablePicCache.htm)）

函数原型:  
  
long LoadPic(pic\_name)

参数定义:  
  
pic\_name 字符串: 文件名
比如"1.bmp|2.bmp|3.bmp" 等,可以使用通配符,比如

         
"\*.bmp" 这个对应了所有的bmp文件

         
"a?c\*.bmp" 这个代表了所有第一个字母是a 第三个字母是c 第二个字母任意的所有bmp文件

         
"abc???.bmp|1.bmp|aa??.bmp"
可以这样任意组合.

返回值:

整形数:  
0:失败  
1:成功

示例:

PutAttachment "c:\test","\*.bmp"  
dm\_ret = dm.SetPath("c:\test")

all\_pic = "abc???.bmp|1.bmp|aa??.bmp"  
dm\_ret = dm.LoadPic(all\_pic)

注: 如果在LoadPic后(图片名为相对路径时)，又设置SetPath为别的目录，会导致加入缓存的图片失效，等于没加载.