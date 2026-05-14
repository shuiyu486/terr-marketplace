# FindPicSimMemEx

**分类:** 图色

**签名:** `string FindPicSimMemEx(x1, y1, x2, y2, pic_info, delta_color,sim,dir)`

**描述:** 查找指定区域内的图片,位图必须是24位色格式,支持透明色,当图像上下左右4个顶点的颜色一样时,则这个颜色将作为透明色处理.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| pic_info | str | 图片数据地址集合. 格式为"地址1,长度1|地址2,长度2.....|地址n,长度n". 可以用[AppendPicAddr](AppendPicAddr.htm)来组合. 地址表示24位位图资源在内存中的首地址，用十进制的数值表示 长度表示位图资源在内存中的长度，用十进制数值表示. |
| delta_color | str | 颜色色偏 比如"203040" 表示RGB的色偏分别是20 30 40 (这里是16进制表示) . 如果这里的色偏是2位，表示使用灰度找图. 比如"20" |
| sim | int | 最小百分比相似率. 表示匹配的颜色占总颜色数的百分比. 其中透明色也算作匹配色. 取值为0到100. 100表示必须完全匹配. 0表示任意颜色都匹配. 只有大于sim的相似率的才会被匹配 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |

## 返回值

- 返回的是所有找到的坐标格式如下:"id,sim,x,y|id,sim,x,y..|id,sim,x,y" (图片左上角的坐标) 比如"0,82,100,20|2,70,30,40" 表示找到了两个,第一个,对应的图片是图像序号为0的图片,坐标是(100,20),当前匹配百分比是82,第二个是序号为2的图片,坐标(30,40),当前匹配百分比是70 (由于内存限制,返回的图片数量最多为1500个左右)

## 示例

```vbs
pic_info = ""
pic_info = dm.AppendPicAddr(pic_info,12034,643)
pic_info = dm.AppendPicAddr(pic_info,328435,8935)
pic_info = dm.AppendPicAddr(pic_info,809234,789)
dm_ret = dm.FindPicSimMemEx(0,0,2000,2000, pic_info,"020202",80,0)
If len(dm_ret) > 0 Then
ss =
split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
TracePrint
ss(index)
sss =
split(ss(index),",")
id =
int(sss(0))
sim =
int(sss(1))
x =
int(sss(2))
y =
int(sss(3))
dm.MoveTo
x,y
Delay 1000
index =
index+1
Loop
End If

注 : 内存中的图片格式必须是24位色，并且不能加密.
此接口和FindPicMemEx类似. 只不过FindPicSimMemEx是以颜色百分比来进行匹配. 如果待查找区域内有杂色,只要颜色百分比达到要求,也一样可以匹配.

这个接口是FindPicMemEx的进阶版本. 当sim为100时,那么FindPicSimMemEx就退化为FindPicMemEx
此接口速度很慢,因为需要搜索任何一种可能. 所以尽可能把搜索范围要小一些. 以免耗时太长.
```
