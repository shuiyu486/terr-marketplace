# CheckFontSmooth

**分类:** 系统

**签名:** `long CheckFontSmooth()`

**描述:** 检测当前系统是否有开启屏幕字体平滑.

## 参数

*此函数无参数。*

## 返回值

- 0 : 系统没开启平滑字体.
- 1 : 系统有开启平滑字体.

## 示例

```vbs
if dm.CheckFontSmooth () = 1 then
TracePrint
"当前系统有开启平滑字体"
end if
```
