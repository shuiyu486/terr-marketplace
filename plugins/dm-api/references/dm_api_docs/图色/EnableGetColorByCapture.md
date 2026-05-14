# EnableGetColorByCapture

**分类:** 图色

**签名:** `long EnableGetColorByCapture(enable)`

**描述:** 允许调用GetColor GetColorBGR GetColorHSV 以及 CmpColor时，以截图的方式来获取颜色。 默认关闭.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm.EnableGetColorByCapture 1
TracePrint dm.GetColor(300,300)

注 : 某些窗口上，可能GetColor会获取不到颜色，可以尝试此接口.
```
