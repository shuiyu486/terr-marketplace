# ScreenToClient

**分类:** 窗口

**签名:** `long ScreenToClient(hwnd,x,y)`

**描述:** 把屏幕坐标转换为窗口坐标

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| x | int* | 屏幕X坐标 |
| y | int* | 屏幕Y坐标 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
x = 100:y = 100
dm_ret = dm.ScreenToClient(hwnd,x,y)
```
