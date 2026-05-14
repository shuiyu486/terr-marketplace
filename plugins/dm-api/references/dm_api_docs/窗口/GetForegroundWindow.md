# GetForegroundWindow

**分类:** 窗口

**签名:** `long GetForegroundWindow()`

**描述:** 获取顶层活动窗口,可以获取到按键自带插件无法获取到的句柄

## 参数

*此函数无参数。*

## 返回值

- 返回整型表示的窗口句柄

## 示例

```vbs
hwnd = dm.GetForegroundWindow()
```
