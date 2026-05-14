大漠插件,建议大家用VBS的方式来调用,具体调用规范如下,两种方式可以结合使用

1.    
无返回值的不能带括号 ,或者说无括号不能带返回值,例如

dm.FindStr
0,0,2000,2000,"长安","aaaaa-00000",1.0,intX,intY

dm.MoveTo intX,intY

dm.LeftClick

dm.SetPath
"c:\xxxx"

dm.SetDict
0,"test.txt"

dm.LoadPic
"\*.bmp"

等等,这些都是不需要返回值的,那么不需要加括号,当然,你也可以加括号,但是就必须遵循规则2

2.    
有返回值的必须带括号,或者说,有括号必须有返回值,例如

dm\_ret
= dm.FindStr(0,0,2000,2000,"长安","aaaaa-00000",1.0,intX,intY)

dm\_ret
= dm.MoveTo(intX,intY)

dm\_ret
= dm.LeftClick()

dm\_ret
= dm.SetPath("c:\xxxx")

dm\_ret
= dm.SetDict(0,"test.txt")

dm\_ret
= dm.LoadPic("\*.bmp")

有些函数,是必须有返回值的,那么就必须带括号,比如Ocr函数等

ss = dm.Ocr(0,0,2000,2000,"aaaaaa-000000",1.0)