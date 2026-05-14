# FindMultiColor

**分类:** 图色

**签名:** `long FindMultiColor(x1, y1, x2, y2,first_color,offset_color,sim, dir,intX,intY)`

**描述:** 根据指定的多点查找颜色坐标

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| first_color | str | 颜色 格式为"RRGGBB-DRDGDB|RRGGBB-DRDGDB|…………",比如"123456-000000" 这里的含义和按键自带Color插件的意义相同，只不过我的可以支持偏色和多种颜色组合 所有的偏移色坐标都相对于此颜色.注意，这里只支持RGB颜色. |
| offset_color | str | 偏移颜色 可以支持任意多个点 格式和按键自带的Color插件意义相同, 只不过我的可以支持偏色和多种颜色组合 格式为"x1|y1|RRGGBB-DRDGDB|RRGGBB-DRDGDB……,……xn|yn|RRGGBB-DRDGDB|RRGGBB-DRDGDB……" 比如"1|3|aabbcc|aaffaa-101010,-5|-3|123456-000000|454545-303030|565656"等任意组合都可以，支持偏色 还可以支持反色模式，比如"1|3|-aabbcc|-334455-101010,-5|-3|-123456-000000|-353535|454545-101010","-"表示除了指定颜色之外的颜色. |
| sim | double | 相似度,取值范围0.1-1.0 |
| dir | int | 查找方向 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上 |
| intX | int* | 返回X坐标(坐标为first_color所在坐标) |
| intY | int* | 返回Y坐标(坐标为first_color所在坐标) |

## 返回值

- 0:没找到
- 1:找到

## 示例

```vbs
dm_ret = dm.FindMultiColor(0,0,2000,2000,"cc805b-020202|606060-010101","9|2|-00ff00|-ff0000,15|2|2dff1c-010101,6|11|a0d962|aabbcc,11|14|-ffffff",1.0,1,intX,intY)
dm.MoveTo intX,intY
```
