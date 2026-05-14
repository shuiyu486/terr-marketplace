# FoobarStartGif

**分类:** Foobar

**签名:** `long FoobarStartGif(hwnd,x,y,pic_name,repeat_limit,delay)`

**描述:** 在指定的Foobar窗口绘制gif动画.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| pic_name | str | 图像文件名 [如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制](mailto:如果第一个字符是@,则采用指针方式.%20@后面是指针地址和大小.%20必须是十进制). 具体看下面的例子 |
| repeat_limit | int | 表示重复GIF动画的次数，如果是0表示一直循环显示.大于0，则表示循环指定的次数以后就停止显示. |
| delay | int | 表示每帧GIF动画之间的时间间隔.如果是0，表示使用GIF内置的时间，如果大于0，表示使用自定义的时间间隔. |

## 返回值

- 整形数 :
- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarStartGif(foobar,0,0,"警报.gif",0,0)

dm_ret = dm.FoobarStartGif(foobar,0,0,"@23432525,2345",0,0)

注 : 当foobar关闭时，所有播放的gif也会自动关闭，内部资源也会自动释放，没必要一定去调用FoobarStopGif函数.

另外，所有gif动画是在顶层显示，在默认绘图层和Print层之上. gif之间的显示顺序按照调用FoobarStartGif的顺序决定.
```
