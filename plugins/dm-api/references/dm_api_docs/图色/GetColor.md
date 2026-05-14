# GetColor

**分类:** 图色

**签名:** `string GetColor(x,y)`

**描述:** 获取(x,y)的颜色,颜色返回格式"RRGGBB",注意,和按键的颜色格式相反

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x | int | X坐标 |
| y | int | Y坐标 |

## 返回值

- 颜色字符串(注意这里都是小写字符，和工具相匹配)

## 示例

```vbs
color = dm.GetColor(30,30)
If color = "ffffff" Then
MessageBox
"是白色"
End If
```
