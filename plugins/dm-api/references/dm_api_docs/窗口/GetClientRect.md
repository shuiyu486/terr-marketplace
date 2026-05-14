# GetClientRect

**分类:** 窗口

**签名:** `long GetClientRect(hwnd,x1,y1,x2,y2)`

**描述:** 获取窗口客户区域在屏幕上的位置

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| x1 | int* | 返回窗口客户区左上角X坐标 |
| y1 | int* | 返回窗口客户区左上角Y坐标 |
| x2 | int* | 返回窗口客户区右下角X坐标 |
| y2 | int* | 返回窗口客户区右下角Y坐标 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.GetClientRect(hwnd,x1,y1,x2,y2)
```
