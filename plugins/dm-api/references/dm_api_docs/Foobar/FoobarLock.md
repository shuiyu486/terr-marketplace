# FoobarLock

**分类:** Foobar

**签名:** `long FoobarLock(hwnd)`

**描述:** 锁定指定的Foobar窗口,不能通过鼠标来移动

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarLock(foobar)
```
