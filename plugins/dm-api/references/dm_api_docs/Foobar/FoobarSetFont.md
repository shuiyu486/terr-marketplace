# FoobarSetFont

**分类:** Foobar

**签名:** `long FoobarSetFont(hwnd,font_name,size,flag)`

**描述:** 设置指定Foobar窗口的字体

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| font_name | str | 系统字体名,注意,必须保证系统中有此字体 |
| size | int | 字体大小 |
| flag | int | 取值定义如下 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarSetFont(foobar,"宋体",25,2+4)
```
