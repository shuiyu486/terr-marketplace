# FoobarFillRect

**分类:** Foobar

**签名:** `long FoobarFillRect(hwnd,x1,y1,x2,y2,color)`

**描述:** 在指定的Foobar窗口内部填充矩形

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x1 | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y1 | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| x2 | int | 右下角X坐标(相对于hwnd客户区坐标) |
| y2 | int | 右下角Y坐标(相对于hwnd客户区坐标) |
| color | str | 填充的颜色值 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarFillRect(foobar,0,0,200,200,"FF0000")
```
