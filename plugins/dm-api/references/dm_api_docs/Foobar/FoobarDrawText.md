# FoobarDrawText

**分类:** Foobar

**签名:** `long FoobarDrawText(hwnd,x,y,w,h,text,color,align)`

**描述:** 在指定的Foobar窗口绘制文字

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| w | int | 矩形区域的宽度 |
| h | int | 矩形区域的高度 |
| text | str | 字符串 |
| color | str | 文字颜色值 |
| align | int | 取值定义如下 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarDrawText(foobar,0,0,200,30,"测试","FF0000",1)
```
