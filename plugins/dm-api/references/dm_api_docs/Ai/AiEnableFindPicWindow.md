函数简介:

设置是否在调用AiFindPicXX系列接口时,是否弹出找图结果的窗口.  方便调试. 默认是关闭的.

函数原型:  
  
long AiEnableFindPicWindow(enable)

参数定义:

enable 整形数: 0 关闭  
1 开启

返回值:

整形数:  
0: 失败  
1: 成功

示例:

set dm =
CreateObject("dm.dmsoft")

TracePrint dm.Ver()

dm.AiEnableFindPicWindow 1

ai\_path = "D:\ai.module"

dm\_ret = dm.LoadAi(ai\_path)

TracePrint dm\_ret

dm.SetPath dm.GetBasePath()

dm\_ret =
dm.FreePic("souce.bmp")

dm\_ret =
dm.SetDisplayInput("pic:souce.bmp")

dm\_ret =
dm.AiFindPic(0,0,2000,2000,"test.bmp",0.8,0,x,y)

TracePrint x &","&y

dm\_ret =
dm.AiFindPicEx(0,0,2000,2000,"test.bmp",0.8,0)

TracePrint dm\_ret

dm\_ret =
dm.SetDisplayInput("screen")

这是一个从图片中找图片的例子.