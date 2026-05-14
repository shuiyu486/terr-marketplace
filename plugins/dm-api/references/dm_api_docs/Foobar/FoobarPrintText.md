# FoobarPrintText

**分类:** Foobar

**签名:** `long FoobarPrintText(hwnd,text,color)`

**描述:** 向指定的Foobar窗口区域内输出滚动文字

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| text | str | 文本内容 |
| color | str | 文本颜色 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarPrintText(foobar,"大漠测试","ff0000")

// 用红色文字向滚动区域输出文字信息
```
