# UnBindWindow

**分类:** 后台设置

**签名:** `long UnBindWindow()`

**描述:** 解除绑定窗口,并释放系统资源.一般在OnScriptExit调用

## 参数

*此函数无参数。*

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
Sub OnScriptExit()
dm_ret = dm.UnBindWindow()
End Sub
```
