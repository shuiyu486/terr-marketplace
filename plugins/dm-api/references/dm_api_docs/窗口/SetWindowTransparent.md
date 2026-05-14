# SetWindowTransparent

**分类:** 窗口

**签名:** `long SetWindowTransparent(hwnd,trans)`

**描述:** 设置窗口的透明度

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| trans | int | 透明度 取值(0-255) 越小透明度越大 0为完全透明(不可见) 255为完全显示(不透明) |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.SetWindowTransparent(hwnd,200)

注 :  此接口不支持WIN98
```
