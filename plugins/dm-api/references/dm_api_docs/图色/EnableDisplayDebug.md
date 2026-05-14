# EnableDisplayDebug

**分类:** 图色

**签名:** `long EnableDisplayDebug(enable_debug)`

**描述:** 开启图色调试模式，此模式会稍许降低图色和文字识别的速度.默认不开启.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable_debug | int | 0 为关闭 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.EnableDisplayDebug 1
dm_ret = dm.CapturePre("screen.bmp")
```
