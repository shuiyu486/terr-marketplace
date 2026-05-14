# FoobarDrawLine

**分类:** Foobar

**签名:** `long FoobarDrawLine(hwnd,x1,y1,x2,y2,color,style,width)`

**描述:** 在指定的Foobar窗口内部画线条.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x1 | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y1 | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| x2 | int | 右下角X坐标(相对于hwnd客户区坐标) |
| y2 | int | 右下角Y坐标(相对于hwnd客户区坐标) |
| color | str | 填充的颜色值 |
| style | int | 画笔类型. 0为实线. 1为虚线 |
| width | int | 线条宽度. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarDrawLine(foobar,0,0,200,200,"FF0000",1,1)
```

## 注意

- 当style为1时，线条宽度必须也是1.否则线条是实线.
