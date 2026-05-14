# MatchPicName

**分类:** 图色

**签名:** `string MatchPicName(pic_name)`

**描述:** 根据通配符获取文件集合. 方便用于FindPic和FindPicEx

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pic_name | str | 文件名 比如"1.bmp|2.bmp|3.bmp" 等,可以使用通配符,比如 "\*.bmp" 这个对应了所有的bmp文件 "a?c\*.bmp" 这个代表了所有第一个字母是a 第三个字母是c 第二个字母任意的所有bmp文件 "abc???.bmp|1.bmp|aa??.bmp" 可以这样任意组合. |

## 返回值

- 返回的是通配符对应的文件集合，每个图片以|分割

## 示例

```vbs
PutAttachment "c:\test","\*.bmp"
dm_ret = dm.SetPath("c:\test")

all_pic = "abc\*.bmp"
pic_name = dm.MatchPicName(all_pic)

// 比如c:\test目录下有abc001.bmp
abc002.bmp abc003.bmp

// 那么pic_name 的值为abc001.bmp|abc002.bmp|abc003.bmp
```
