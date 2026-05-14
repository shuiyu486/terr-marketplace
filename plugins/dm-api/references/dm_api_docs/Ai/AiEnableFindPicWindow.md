# AiEnableFindPicWindow

**分类:** Ai

**签名:** `long AiEnableFindPicWindow(enable)`

**描述:** 设置是否在调用AiFindPicXX系列接口时,是否弹出找图结果的窗口.  方便调试. 默认是关闭的.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
set dm =
CreateObject("dm.dmsoft")

TracePrint dm.Ver()

dm.AiEnableFindPicWindow 1

ai_path = "D:\ai.module"

dm_ret = dm.LoadAi(ai_path)

TracePrint dm_ret

dm.SetPath dm.GetBasePath()

dm_ret = dm.FreePic("souce.bmp")

dm_ret = dm.SetDisplayInput("pic:souce.bmp")

dm_ret = dm.AiFindPic(0,0,2000,2000,"test.bmp",0.8,0,x,y)

TracePrint x &","&y

dm_ret = dm.AiFindPicEx(0,0,2000,2000,"test.bmp",0.8,0)

TracePrint dm_ret

dm_ret = dm.SetDisplayInput("screen")

这是一个从图片中找图片的例子.
```
