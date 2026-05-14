# GetPointWindow

**分类:** 窗口

**签名:** `long GetPointWindow(x,y)`

**描述:** 获取给定坐标的可见窗口句柄,可以获取到按键自带的插件无法获取到的句柄

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| X | int | 屏幕X坐标 |
| Y | int | 屏幕Y坐标 |

## 返回值

- 返回整型表示的窗口句柄

## 示例

```vbs
hwnd = dm.GetPointWindow(100,100)
```
