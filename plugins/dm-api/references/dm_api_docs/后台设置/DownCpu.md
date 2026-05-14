# DownCpu

**分类:** 后台设置

**签名:** `long DownCpu(type,rate)`

**描述:** 降低目标窗口所在进程的CPU占用.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| type | int | 当取值为0时,rate取值范围大于等于0 ,这个值越大表示降低CPU效果越好 当取值为1时,rate取值范围大于等于0,表示以固定的FPS来降低CPU. rate表示FPS.  并且这时不能有dx.public.down.cpu. |
| rate | int | 取值取决于type. 为0表示关闭 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindowEx(hwnd,"dx.graphic.3d","normal","normal","",0)
dm.DownCpu 1,10

dm_ret = dm.BindWindowEx(hwnd,"normal","normal","normal","dx.public.down.cpu",101)
dm.DownCpu 0,50
```

## 注意

- 此接口必须在绑定窗口成功以后调用，而且必须保证目标窗口可以支持dx.graphic.3d或者dx.graphic.3d.8或者dx.graphic.2d或者dx.graphic.2d.2或者dx.graphic.opengl或者dx.graphic.opengl.esv2方式截图，或者使用dx.public.down.cpu(仅限type为0).否则降低CPU无效.
- 因为降低CPU是通过降低窗口刷新速度或者在系统消息循环增加延时来实现，所以注意，开启此功能以后会导致窗口刷新速度变慢.
