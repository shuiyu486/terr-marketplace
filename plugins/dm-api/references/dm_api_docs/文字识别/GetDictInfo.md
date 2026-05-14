函数简介:

根据指定的文字，以及指定的系统字库信息，获取字库描述信息.

函数原型:  
  
string GetDictInfo(str,font\_name,font\_size,flag)

参数定义:

str 字符串:需要获取的字符串  
font\_name 字符串:系统字体名,比如"宋体"  
font\_size 整形数:系统字体尺寸，这个尺寸一定要以大漠综合工具获取的为准.如何获取尺寸看视频教程.  
flag 整形数:字体类别 取值可以是以下值的组合,比如1+2+4+8,2+4.
0表示正常字体.  
    1 : 粗体  
    2 : 斜体  
    4 : 下划线  
    8 : 删除线

返回值:

字符串:  
返回字库信息,每个字符的字库信息用"|"来分割

示例:

// 下面的代码是获取"回收站"这3个字符的字库信息，然后加入到字库1中.  
font\_desc = dm.GetDictInfo("回收站","宋体",9,0)  
font\_desc = split(font\_desc,"|")  
count = ubound(font\_desc)  
for i = 0 to count  
    TracePrint
font\_desc(i)  
    dm.AddDict
1,font\_desc(i)  
next