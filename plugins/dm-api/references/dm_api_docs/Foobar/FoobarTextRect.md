# FoobarTextRect

**分类:** Foobar

**签名:** `long FoobarTextRect(hwnd,x,y,w,h)`

**描述:** 设置指定Foobar窗口的滚动文本框范围,默认的文本框范围是窗口区域

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| x | int | x坐标 |
| y | int | y坐标 |
| w | int | 宽度 |
| h | int | 高度 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarTextRect(foobar,10,10,100,200)
```
