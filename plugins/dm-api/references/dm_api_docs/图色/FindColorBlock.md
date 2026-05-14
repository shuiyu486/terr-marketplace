# FindColorBlock

**分类:** 图色

**签名:** `long FindColorBlock(x1, y1, x2, y2, color, sim, count,width,height,intX,intY)`

**描述:** 查找指定区域内的颜色块,颜色格式"RRGGBB-DRDGDB",注意,和按键的颜色格式相反

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| color | str | 颜色 格式为"RRGGBB-DRDGDB",比如"123456-000000|aabbcc-202020".也可以支持反色模式. 前面加@即可. 比如"@123456-000000|aabbcc-202020". 具体可以看下放注释.注意，这里只支持RGB颜色. |
| sim | double | 相似度,取值范围0.1-1.0 |
| count | int | 在宽度为width,高度为height的颜色块中，符合color颜色的最小数量.(注意,这个颜色数量可以在综合工具的二值化区域中看到) |
| width | int | 颜色块的宽度 |
| height | int | 颜色块的高度 |
| intX | int* | 返回X坐标(指向颜色块的左上角) |
| intY | int* | 返回Y坐标(指向颜色块的左上角) |

## 返回值

- 0:没找到
- 1:找到

## 示例

```vbs
dm_ret = dm.FindColorBlock(0,0,2000,2000,"123456-000000|aabbcc-030303|ddeeff-202020",1.0,350,100,200,intX,intY)
If intX >= 0 and intY
>= 0 Then
MessageBox
"找到"
End If
```

## 注意

- 反色模式是指匹配任意一个指定颜色之外的颜色. 比如"@123456|333333". 在匹配时,会匹配除了123456或者333333之外的颜色.
