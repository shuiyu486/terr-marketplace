# GetPicSize

**分类:** 图色

**签名:** `string GetPicSize(pic_name)`

**描述:** 获取指定图片的尺寸，如果指定的图片已经被加入缓存，则从缓存中获取信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pic_name | str | 文件名 比如"1.bmp" |

## 返回值

- 形式如 "w,h" 比如"30,20"

## 示例

```vbs
PutAttachment "c:\test","\*.bmp"
dm_ret = dm.SetPath("c:\test")

pic_size = dm.GetPicSize("1.bmp")
pic_size = split(pic_size,",")
w = int(pic_size(0))
h = int(pic_size(1))
Trace "宽度:"&w
Trace "高度:"&h
```
