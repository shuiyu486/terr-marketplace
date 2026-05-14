# SetLocale

**分类:** 系统

**签名:** `long SetLocale()`

**描述:** 设置当前系统的非UNICOD字符集. 会弹出一个字符集选择列表,用户自己选择到简体中文即可.

## 参数

*此函数无参数。*

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
if dm.GetLocale() = 0 then
dm.SetLocale()
dm.ExitOs(2)
end if
```
