# FoobarClose

**分类:** Foobar

**签名:** `long FoobarClose(hwnd)`

**描述:** 关闭一个Foobar,注意,必须调用此函数来关闭窗口,用SetWindowState也可以关闭,但会造成内存泄漏.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.FoobarClose(foobar)
```
