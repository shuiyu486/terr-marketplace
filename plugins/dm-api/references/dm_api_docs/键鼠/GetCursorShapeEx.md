# GetCursorShapeEx

**分类:** 键鼠

**签名:** `string GetCursorShapeEx(int type)`

**描述:** 获取鼠标特征码. 当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| type | int | 获取鼠标特征码的方式. 和工具中的方式1 方式2对应. 方式1此参数值为0. 方式2此参数值为1. |

## 返回值

- 成功时，返回鼠标特征码. 失败时，返回空的串.

## 示例

```vbs
mouse_tz = dm.GetCursorShapeEx(0)
If mouse_tz = "7d7160fe" Then
MessageBox
"找到特征码"
End If
```

## 注意

- 当type为0时，和GetCursorShape等效.
- 另要特别注意,WIN7以及以上系统，必须在字体显示设置里把文字大小调整为默认(100%),否则特征码会变.如图所示.
