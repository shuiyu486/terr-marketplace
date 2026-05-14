# CaptureGif

**分类:** 图色

**签名:** `long CaptureGif(x1, y1, x2, y2, file,delay,time)`

**描述:** 抓取指定区域(x1, y1, x2, y2)的动画，保存为gif格式

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| file | str | 保存的文件名,保存的地方一般为SetPath中设置的目录 当然这里也可以指定全路径名. |
| delay | int | 动画间隔，单位毫秒。 如果为0，表示只截取静态图片 |
| time | int | 总共截取多久的动画，单位毫秒。 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
// 截取动画
dm_ret = dm.CaptureGif(0,0,2000,2000,"screen.gif",100,3000)

// 截取静态
dm_ret = dm.CaptureGif(0,0,2000,2000,"screen.gif",0,0)
```
