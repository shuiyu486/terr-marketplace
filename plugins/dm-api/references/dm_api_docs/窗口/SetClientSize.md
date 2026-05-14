# SetClientSize

**分类:** 窗口

**签名:** `long SetClientSize(hwnd,width,height)`

**描述:** 设置窗口客户区域的宽度和高度

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| width | int | 宽度 |
| height | int | 高度 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.SetClientSize(hwnd,800,600)
```
