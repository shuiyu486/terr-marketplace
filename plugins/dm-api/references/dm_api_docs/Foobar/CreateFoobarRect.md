# CreateFoobarRect

**分类:** Foobar

**签名:** `long CreateFoobarRect(hwnd,x,y,w,h)`

**描述:** 创建一个矩形窗口

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| w | int | 矩形区域的宽度 |
| h | int | 矩形区域的高度 |

## 返回值

- 整形数 : 创建成功的窗口句柄

## 示例

```vbs
foobar = dm.CreateFoobarRect(hwnd,10,10,200,200)
```

## 注意

- foobar不能在本进程窗口内创建.
