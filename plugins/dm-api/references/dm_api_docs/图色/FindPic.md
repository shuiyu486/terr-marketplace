# FindPic

**分类:** 图色

**签名:** `long FindPic(x1, y1, x2, y2, pic_name, delta_color,sim, dir,intX, intY)`

**描述:** 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| pic_name | str | 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp" |
| delta_color | str | 颜色色偏 比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示). 如果这里的色偏是2位，表示使用灰度找图. 比如"20" |
| sim | double | 相似度,取值范围0.1-1.0 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |
| intX | int* | 返回图片左上角的X坐标 |
| intY | int* | 返回图片左上角的Y坐标 |

## 返回值

- 返回找到的图片的序号,从0开始索引.如果没找到返回-1

## 示例

```vbs
dm_ret = dm.FindPic(0,0,2000,2000,"1.bmp|2.bmp|3.bmp","000000",0.9,0,intX,intY)
If intX >= 0 and intY >= 0 Then
MessageBox "找到"
End If
```
