# FoobarClearText

**分类:** Foobar

**签名:** `long FoobarClearText(hwnd)`

**描述:** 清除指定的Foobar滚动文本区

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |

## 返回值

- 整形数 :
- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarClearText(foobar)
```
