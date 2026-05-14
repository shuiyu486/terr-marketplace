# FoobarTextLineGap

**分类:** Foobar

**签名:** `long FoobarTextLineGap(hwnd,line_gap)`

**描述:** 设置滚动文本区的文字行间距,默认是3

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| line_gap | int | 文本行间距 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarTextLineGap(foobar,5)
```
