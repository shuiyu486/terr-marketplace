# OcrInFile

**分类:** 文字识别

**签名:** `string OcrInFile(x1, y1, x2, y2, pic_name, color_format, sim)`

**描述:** 识别位图中区域(x1,y1,x2,y2)的文字

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| pic_name | str | 图片文件名 |
| color_format | str | 颜色格式串.注意，RGB和HSV,以及灰度格式都支持. |
| sim | double | 相似度,取值范围0.1-1.0 |

## 返回值

- 返回识别到的字符串

## 示例

```vbs
s = dm.OcrInFile(0,0,2000,2000,"test.bmp","000000-000000",1.0)
MessageBox s
```
