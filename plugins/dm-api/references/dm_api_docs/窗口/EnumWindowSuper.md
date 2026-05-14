# EnumWindowSuper

**分类:** 窗口

**签名:** `string EnumWindowSuper(spec1,flag1,type1,spec2,flag2,type2,sort)`

**描述:** 根据两组设定条件来枚举指定窗口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| spec1 | str | 查找串1. (内容取决于flag1的值) |
| flag1 | int | 取值如下: |
| type1 | int | 取值如下 |
| spec2 | str | 查找串2. (内容取决于flag2的值) |
| flag2 | int | 取值如下: |
| type2 | int | 取值如下 |
| sort | int | 取值如下 |

## 返回值

- 返回所有匹配的窗口句柄字符串,格式"hwnd1,hwnd2,hwnd3"

## 示例

```vbs
hwnds = dm.EnumWindowSuper("记事本",0,1,"notepad",1,0,0)

hwnds = split(hwnds,",")

转换为数组后,就可以处理了

这里注意,hwnds数组里的是字符串,要用于使用,比如BindWindow时,还得强制类型转换,比如int(hwnds(0))
```
