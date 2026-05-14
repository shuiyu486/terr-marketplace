# GetLocale

**分类:** 系统

**签名:** `long GetLocale()`

**描述:** 判断当前系统使用的非UNICODE字符集是否是GB2312(简体中文)(由于设计插件时偷懒了,使用的是非UNICODE字符集，导致插件必须运行在GB2312字符集环境下).

## 参数

*此函数无参数。*

## 返回值

- 0 : 不是GB2312(简体中文)
- 1 : 是GB2312(简体中文)

## 示例

```vbs
if dm.GetLocale() = 0 then
dm.SetLocale()
dm.ExitOs(2)
end if
```
