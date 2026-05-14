# FaqCaptureFromFile

**分类:** 答题

**签名:** `long FaqCaptureFromFile(x1, y1, x2, y2, file, quality)`

**描述:** 截取指定图片中的图像,并返回此句柄.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 左上角X坐标 |
| y1 | int | 左上角Y坐标 |
| x2 | int | 右下角X坐标 |
| y2 | int | 右下角Y坐标 |
| file | str | 图片文件名,图像格式基本都支持. |
| quality | int | 图像或动画品质,或者叫压缩率,此值越大图像质量越好 取值范围（1-100或者250）.当此值为250时,会截取无损bmp图像数据. |

## 返回值

- 图像或者动画句柄

## 示例

```vbs
handle =
dm.FaqCaptureFromFile(0,0,2000,2000,"c:\test.bmp",50)
```

## 注意

- 如果上一次的FaqPost还没有处理完毕,那么此函数调用会失败,要释放上一次的FaqPost,请调用FaqCancel函数
