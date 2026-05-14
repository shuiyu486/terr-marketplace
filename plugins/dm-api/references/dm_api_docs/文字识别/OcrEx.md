# OcrEx

**分类:** 文字识别

**签名:** `string OcrEx(x1,y1,x2,y2,color_format,sim)`

**描述:** 识别屏幕范围(x1,y1,x2,y2)内符合color_format的字符串,并且相似度为sim,sim取值范围(0.1-1.0),

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| color_format | str | 颜色格式串.注意，RGB和HSV,以及灰度格式都支持. |
| sim | double | 相似度,取值范围0.1-1.0 |

## 返回值

- 返回识别到的字符串 格式如  "字符0$x0$y0|…|字符n$xn$yn"

## 示例

```vbs
和Ocr函数相同，只是结果处理有所不同
如下

dm_ret = dm.OcrEx(0,0,2000,2000,"ffffff|000000",1.0)
ss = split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
TracePrint
ss(index)
sss
= split(ss(index),"$")
ocr_s
= int(sss(0))
x = int(sss(1))
y = int(sss(2))
TracePrint
ocr_s & ","&x&","&y
index = index+1
Loop
```

## 注意

- OcrEx不再像Ocr一样,支持换行分割了.
