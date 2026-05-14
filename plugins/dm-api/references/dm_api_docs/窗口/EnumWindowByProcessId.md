# EnumWindowByProcessId

**分类:** 窗口

**签名:** `string EnumWindowByProcessId(pid,title,class_name,filter)`

**描述:** 根据指定进程pid以及其它条件,枚举系统中符合条件的窗口,可以枚举到按键自带的无法枚举到的窗口

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| pid | int | 进程pid. |
| title | str | 窗口标题. 此参数是模糊匹配. |
| class_name | str | 窗口类名. 此参数是模糊匹配. |
| filter | int | 取值定义如下 |

## 返回值

- 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"

## 示例

```vbs
hwnds = dm.EnumWindowByProcessId(1124,"天龙八部","",1+8+16)

这句是获取到所有标题栏中有"天龙八部"这个字符串的窗口句柄集合,并且所在进程是1124指定的进程.

hwnds = split(hwnds,",")

转换为数组后,就可以处理了

这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))
```
