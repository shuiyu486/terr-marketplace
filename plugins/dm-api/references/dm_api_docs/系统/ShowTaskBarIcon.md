# ShowTaskBarIcon

**分类:** 系统

**签名:** `long ShowTaskBarIcon(hwnd,is_show)`

**描述:** 显示或者隐藏指定窗口在任务栏的图标.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| is_show | int | 0为隐藏,1为显示 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 显示
dm.ShowTaskBarIcon hwnd,1

// 隐藏
dm.ShowTaskBarIcon hwnd,0
```
