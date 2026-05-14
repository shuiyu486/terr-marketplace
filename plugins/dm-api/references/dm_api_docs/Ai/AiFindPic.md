# AiFindPic

**分类:** Ai

**签名:** `long AiFindPic(x1, y1, x2, y2, pic_name,sim, dir,intX, intY)`

**描述:** 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| pic_name | str | 图片名,可以是多个图片,比如"test.bmp|test2.bmp|test3.bmp" |
| sim | double | 相似度,取值范围0.1-1.0 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |
| intX | int* | 返回图片左上角的X坐标 |
| intY | int* | 返回图片左上角的Y坐标 |

## 返回值

- 返回找到的图片的序号,从0开始索引.如果没找到返回-1

## 示例

```vbs
dm_ret = dm.AiFindPic(0,0,2000,2000,"1.bmp|2.bmp|3.bmp",0.9,0,intX,intY)
If intX >= 0 and intY >= 0 Then
MessageBox "找到"
End If

此接口需要ai.module
4.0及其之后的版本.
```
