# LockDisplay

**分类:** 后台设置

**签名:** `long LockDisplay(lock)`

**描述:** 锁定指定窗口的图色数据(不刷新).

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| lock | int | 0关闭锁定 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)
dm.LockDisplay 1
// 这里做需要锁定做的事情
dm.LockDisplay 0
```

## 注意

- 此接口只对图色为dx.graphic.3d  dx.graphic.3d.8
- dx.graphic.2d  dx.graphic.2d.2 dx.graphic.3d.10plus有效.
