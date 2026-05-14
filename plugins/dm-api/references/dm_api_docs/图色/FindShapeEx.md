# FindShapeEx

**分类:** 图色

**签名:** `string FindShapeEx(x1, y1, x2, y2,offset_color,sim, dir)`

**描述:** 查找所有指定的形状的坐标. 形状的描述同按键的抓抓. 具体可以参考按键的抓抓.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| offset_color | str | 坐标偏移描述 可以支持任意多个点 格式和按键自带的Color插件意义相同 格式为"x1|y1|e1,……xn|yn|en" 比如"1|3|1,-5|-3|0"等任意组合都可以 |
| sim | double | 相似度,取值范围0.1-1.0 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |

## 返回值

- 返回所有形状的坐标值,然后通过GetResultCount等接口来解析(由于内存限制,返回的坐标数量最多为1800个左右)

## 示例

```vbs
dm_ret = dm.FindShapeEx(0,0,2000,2000,"1|1|0,1|6|1,0|10|1,9|10|1,7|6|1,7|8|0,8|9|0,2|2|1,3|1|1",1.0,1)
count = dm.GetResultCount(dm_ret)
index = 0
Do While index < count
aa =
dm.GetResultPos(dm_ret,index,intX,intY)
dm.MoveTo intX,intY
index = index + 1
Delay  1000
Loop
```
