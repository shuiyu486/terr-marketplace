# GetColorHSV

**分类:** 图色

**签名:** `string GetColorHSV(x,y)`

**描述:** 获取(x,y)的HSV颜色,颜色返回格式"H.S.V"

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x | int | X坐标 |
| y | int | Y坐标 |

## 返回值

- 颜色字符串

## 示例

```vbs
color = dm.GetColorHSV(30,30)
If color = "100.20.20" Then
MessageBox
"ok"
End If
```
