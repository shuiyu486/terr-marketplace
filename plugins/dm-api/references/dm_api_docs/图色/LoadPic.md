# LoadPic

**分类:** 图色

**签名:** `long LoadPic(pic_name)`

**描述:** 预先加载指定的图片,这样在操作任何和图片相关的函数时,将省去了加载图片的时间。调用此函数后,没必要一定要调用FreePic,插件自己会自动释放.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pic_name | str | 文件名 比如"1.bmp|2.bmp|3.bmp" 等,可以使用通配符,比如 "\*.bmp" 这个对应了所有的bmp文件 "a?c\*.bmp" 这个代表了所有第一个字母是a 第三个字母是c 第二个字母任意的所有bmp文件 "abc???.bmp|1.bmp|aa??.bmp" 可以这样任意组合. |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
PutAttachment "c:\test","\*.bmp"
dm_ret = dm.SetPath("c:\test")

all_pic = "abc???.bmp|1.bmp|aa??.bmp"
dm_ret = dm.LoadPic(all_pic)
```

## 注意

- 如果在LoadPic后(图片名为相对路径时)，又设置SetPath为别的目录，会导致加入缓存的图片失效，等于没加载.
