# ClientToScreen

**分类:** 窗口

**签名:** `long ClientToScreen(hwnd,x,y)`

**描述:** 把窗口坐标转换为屏幕坐标

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| x | int* | 窗口X坐标 |
| y | int* | 窗口Y坐标 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
x = 0:y = 0
dm_ret = dm.ClientToScreen(hwnd,x,y)
```
