# FindPicExS

**分类:** 图色

**签名:** `string FindPicExS(x1, y1, x2, y2, pic_name, delta_color,sim, dir)`

**描述:** 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| pic_name | str | 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp" |
| delta_color | str | 颜色色偏 比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示) . 如果这里的色偏是2位，表示使用灰度找图. 比如"20" |
| sim | double | 相似度,取值范围0.1-1.0 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |

## 返回值

- 返回的是所有找到的坐标格式如下:"file,x,y| file,x,y..| file,x,y" (图片左上角的坐标) 比如"1.bmp,100,20|2.bmp,30,40" 表示找到了两个,第一个,对应的图片是1.bmp,坐标是(100,20),第二个是2.bmp,坐标(30,40) (由于内存限制,返回的图片数量最多为1500个左右)

## 示例

```vbs
dm_ret = dm.FindPicExS(0,0,2000,2000,"test.bmp|test2.bmp|test3.bmp|test4.bmp|test5.bmp","020202",1.0,0)
If len(dm_ret) > 0 Then
ss
= split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
TracePrint ss(index)
sss = split(ss(index),",")
f = sss(0)
x = int(sss(1))
y = int(sss(2))
dm.MoveTo x,y
Delay 1000
index = index+1
Loop
End If
```
