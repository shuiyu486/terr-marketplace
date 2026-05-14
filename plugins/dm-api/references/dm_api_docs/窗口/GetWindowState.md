# GetWindowState

**分类:** 窗口

**签名:** `long GetWindowState(hwnd,flag)`

**描述:** 获取指定窗口的一些属性

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| flag | int | 取值定义如下 |

## 返回值

- 0: 不满足条件
- 1: 满足条件

## 示例

```vbs
dm_ret = dm.GetWindowState(hwnd,3)
If dm_ret = 1 Then
MessageBox
"窗口已经最小化了"
End If
```
