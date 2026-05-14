# FoobarStopGif

**分类:** Foobar

**签名:** `long FoobarStopGif(hwnd,x,y,pic_name)`

**描述:** 停止在指定foobar里显示的gif动画.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口,注意,此句柄必须是通过CreateFoobarxxxx系列函数创建出来的 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| pic_name | str | 图像文件名 |

## 返回值

- 整形数 :
- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.FoobarStopGif(foobar,0,0,"警报.gif")

注 : 当foobar关闭时，所有播放的gif也会自动关闭，内部资源也会自动释放，没必要一定去调用FoobarStopGif函数.

另外，对于在不同的坐标显示的gif动画，插件内部会认为是不同的GIF.所以停止GIF时，一定要和FoobarStartGif时指定的x,y坐标一致.
```
