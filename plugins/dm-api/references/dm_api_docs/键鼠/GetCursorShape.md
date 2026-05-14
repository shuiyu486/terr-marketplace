# GetCursorShape

**分类:** 键鼠

**签名:** `string GetCursorShape()`

**描述:** 获取鼠标特征码. 当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，

## 参数

*此函数无参数。*

## 返回值

- 成功时，返回鼠标特征码. 失败时，返回空的串.

## 示例

```vbs
mouse_tz = dm.GetCursorShape()
If mouse_tz = "7d7160fe" Then
MessageBox
"找到特征码"
End If
```

## 注意

- 此接口和GetCursorShapeEx(0)等效. 相当于工具里的方式1获取的特征码. 当此特征码在某些情况下无法区分鼠标形状时，可以考虑使用GetCursorShapeEx(1).
- 另要特别注意,WIN7以及以上系统，必须在字体显示设置里把文字大小调整为默认(100%),否则特征码会变.如图所示.
