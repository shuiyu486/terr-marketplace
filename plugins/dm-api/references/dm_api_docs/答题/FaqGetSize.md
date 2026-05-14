# FaqGetSize

**分类:** 答题

**签名:** `long FaqGetSize(handle)`

**描述:** 获取句柄所对应的数据包的大小,单位是字节

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| handle | int | 由FaqCapture返回的句柄 |

## 返回值

- 数据包大小,一般用于判断数据大小,选择合适的压缩比率.

## 示例

```vbs
// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms
handle = dm.FaqCapture(intX - 50,intY - 232,intX+272,intY-12,50,100,3000)
packet_size = dm.FaqGetSize(handle)
MessageBox packet_size
```
