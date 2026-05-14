# FoobarUpdate

**分类:** Foobar

**签名:** `long FoobarUpdate(hwnd)`

**描述:** 刷新指定的Foobar窗口

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarUpdate(foobar)

注意： 所有绘制完成以后,必须通过调用此函数来刷新窗口,否则窗口内容不会改变.
```
