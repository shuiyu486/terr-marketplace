函数简介:

获取指定图片的尺寸，如果指定的图片已经被加入缓存，则从缓存中获取信息.  
此接口也会把此图片加入缓存. （当图色缓存机制打开时,具体参考[EnablePicCache](../基本设置/EnablePicCache.htm)）

函数原型:  
  
string GetPicSize(pic\_name)

参数定义:  
  
pic\_name 字符串: 文件名 比如"1.bmp"

返回值:

字符串:  
形式如 "w,h" 比如"30,20"

示例:

PutAttachment "c:\test","\*.bmp"  
dm\_ret = dm.SetPath("c:\test")

pic\_size = dm.GetPicSize("1.bmp")  
pic\_size = split(pic\_size,",")  
w = int(pic\_size(0))  
h = int(pic\_size(1))  
Trace "宽度:"&w  
Trace "高度:"&h