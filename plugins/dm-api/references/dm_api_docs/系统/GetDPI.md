# GetDPI

**分类:** 系统

**签名:** `long GetDPI()`

**描述:** 判断当前系统的DPI(文字缩放)是不是100%缩放.

## 参数

*此函数无参数。*

## 返回值

- 0 : 不是
- 1 : 是

## 示例

```vbs
if dm.GetDPI() = 0 then
MessageBox "当前系统文字缩放不是100%,请设置为100%"
EndScript
end if
```
