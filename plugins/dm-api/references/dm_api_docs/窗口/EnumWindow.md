# EnumWindow

**分类:** 窗口

**签名:** `string EnumWindow(parent,title,class_name,filter)`

**描述:** 根据指定条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| parent | int | 获得的窗口句柄是该窗口的子窗口的窗口句柄,取0时为获得桌面句柄 |
| title | str | 窗口标题. 此参数是模糊匹配. |
| class_name | str | 窗口类名. 此参数是模糊匹配. |
| filter | int | 取值定义如下 |

## 返回值

- 字符串 : 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"

## 示例

```vbs
hwnds = dm.EnumWindow(0,"QQ三国","",1+4+8+16)

这句是获取到所有标题栏中有QQ三国这个字符串的窗口句柄集合

hwnds = split(hwnds,",")

转换为数组后,就可以处理了

这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))
```
