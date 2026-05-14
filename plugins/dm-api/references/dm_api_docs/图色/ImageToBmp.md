# ImageToBmp

**分类:** 图色

**签名:** `long ImageToBmp(pic_name,bmp_name)`

**描述:** 转换图片格式为24位BMP格式.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pic_name | str | 要转换的图片名 |
| bmp_name | str | 要保存的BMP图片名 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm.ImageToBmp "1.png","1.bmp"
dm.ImageToBmp "2.jpg","2.bmp"
dm.ImageToBmp "3.gif","3.bmp"
```
