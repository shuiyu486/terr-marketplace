# MoveWindow

**分类:** 窗口

**签名:** `long MoveWindow(hwnd,x,y)`

**描述:** 移动指定窗口到指定位置

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| x | int | X坐标 |
| y | int | Y坐标 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.MoveWindow hwnd,-10,-10
```
