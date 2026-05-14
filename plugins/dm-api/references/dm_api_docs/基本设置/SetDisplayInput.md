# SetDisplayInput

**分类:** 基本设置

**签名:** `long SetDisplayInput(mode)`

**描述:** 设定图色的获取方式，默认是显示器或者后台窗口(具体参考BindWindow)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| mode | str | 图色输入模式 取值有以下几种 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
// 设定为默认的模式
dm_ret = dm.SetDisplayInput("screen")

// 设定为图片模式 图片采用相对路径模式 相对于SetPath的路径
dm_ret = dm.SetDisplayInput("pic:test.bmp")

// 设为图片模式 图片采用绝对路径模式
dm_ret = dm.SetDisplayInput("pic:d:\test\test.bmp")

// 设为图片模式 但是每次设置前 先清除缓冲
dm_ret = dm.FreePic("test.bmp")
dm_ret = dm.SetDisplayInput("pic:test.bmp")

// 设置为图片模式,图片从内存中获取
dm_ret = dm.SetDisplayInput("mem:1230434,884")
```
