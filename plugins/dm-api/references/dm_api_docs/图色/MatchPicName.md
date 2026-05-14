函数简介:

根据通配符获取文件集合. 方便用于FindPic和FindPicEx

函数原型:  
  
string MatchPicName(pic\_name)

参数定义:  
  
pic\_name 字符串: 文件名
比如"1.bmp|2.bmp|3.bmp" 等,可以使用通配符,比如

         
"\*.bmp" 这个对应了所有的bmp文件

         
"a?c\*.bmp" 这个代表了所有第一个字母是a 第三个字母是c 第二个字母任意的所有bmp文件

         
"abc???.bmp|1.bmp|aa??.bmp" 可以这样任意组合.

返回值:

字符串:  
返回的是通配符对应的文件集合，每个图片以|分割

示例:

PutAttachment "c:\test","\*.bmp"  
dm\_ret = dm.SetPath("c:\test")

all\_pic = "abc\*.bmp"  
pic\_name = dm.MatchPicName(all\_pic)

// 比如c:\test目录下有abc001.bmp
abc002.bmp abc003.bmp

// 那么pic\_name 的值为abc001.bmp|abc002.bmp|abc003.bmp