# FoobarTextPrintDir

**分类:** Foobar

**签名:** `long FoobarTextPrintDir(hwnd,dir)`

**描述:** 设置滚动文本区的文字输出方向,默认是0

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| dir | int | 0 表示向下输出 : 1 表示向上输出 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarTextPrintDir(foobar,1)
```
