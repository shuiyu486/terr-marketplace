# GetAveRGB

**分类:** 图色

**签名:** `string GetAveRGB(x1,y1,x2,y2)`

**描述:** 获取范围(x1,y1,x2,y2)颜色的均值,返回格式"RRGGBB"

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 左上角X |
| y1 | int | 左上角Y |
| x2 | int | 右下角X |
| y2 | int | 右下角Y |

## 返回值

- 颜色字符串

## 示例

```vbs
color = dm.GetAveRGB(30,30,100,100)
MessageBox color
```
