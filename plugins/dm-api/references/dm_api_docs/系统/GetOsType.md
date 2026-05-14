# GetOsType

**分类:** 系统

**签名:** `long GetOsType()`

**描述:** 得到操作系统的类型

## 参数

*此函数无参数。*

## 返回值

- 0 : win95/98/me/nt4.0
- 1 : xp/2000
- 2 : 2003/2003 R2/xp-64
- 3 : vista/2008
- 4 : win7/2008 R2
- 5 : win8/2012
- 6 : win8.1/2012 R2
- 7 : win10/2016 TP/win11

## 示例

```vbs
os_type = dm.GetOsType()
```
