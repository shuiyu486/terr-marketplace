# FetchWord

**分类:** 文字识别

**签名:** `string FetchWord(x1, y1, x2, y2, color, word)`

**描述:** 根据指定的范围,以及指定的颜色描述，提取点阵信息，类似于大漠工具里的单独提取.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 左上角X坐标 |
| y1 | int | 左上角Y坐标 |
| x2 | int | 右下角X坐标 |
| y2 | int | 右下角Y坐标 |
| color | str | 颜色格式串.注意，RGB和HSV,以及灰度格式都支持. |
| word | str | 待定义的文字,不能为空，且不能为关键符号"$" |

## 返回值

- 识别到的点阵信息，可用于AddDict 如果失败，返回空

## 示例

```vbs
info = dm.FetchWord(200,200,250,220,"abcdef-101010|ffffff-101010","张三")
If len(info) > 0 Then
dm.AddDict
3,info
End if

info = dm.FetchWord(200,200,250,220,"b@abcdef-101010|ffffff-101010","李四")
If len(info) > 0 Then
dm.AddDict
2,info
End if

info = dm.FetchWord(200,200,250,220,"b@0.100.100-0.0.0","张三")
If len(info) > 0 Then
dm.AddDict
4,info
End if

info = dm.FetchWord(200,200,250,220,"0.100.100-0.0.0|100.0.0-0.0.0","王")
If len(info) > 0 Then
dm.AddDict
4,info
End if
```
