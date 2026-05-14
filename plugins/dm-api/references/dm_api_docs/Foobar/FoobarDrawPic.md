# FoobarDrawPic

**分类:** Foobar

**签名:** `long FoobarDrawPic(hwnd,x,y,pic_name,trans_color)`

**描述:** 在指定的Foobar窗口绘制图像

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| pic_name | str | 图像文件名 [如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制](mailto:如果第一个字符是@,则采用指针方式.%20@后面是指针地址和大小.%20必须是十进制). 具体看下面的例子 |
| trans_color | str | 图像透明色 |

## 返回值

- 整形数 :
- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarDrawPic(foobar,0,0,"menu.bmp","FF0000")

dm_ret = dm.FoobarDrawPic(foobar,0,0,"@32432525,23435","FF0000")
```
