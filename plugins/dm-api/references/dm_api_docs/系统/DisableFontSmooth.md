# DisableFontSmooth

**分类:** 系统

**签名:** `long DisableFontSmooth()`

**描述:** 关闭当前系统屏幕字体平滑.同时关闭系统的ClearType功能.

## 参数

*此函数无参数。*

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
if dm.CheckFontSmooth()
= 1 then
if dm.DisableFontSmooth()
= 1 then
MessageBox "关闭了当前系统平滑字体,重启生效"
dm.ExitOs 2
Delay 2000
EndScript
end if
end if
```

## 注意

- 关闭之后要让系统生效，必须重启系统才有效.
