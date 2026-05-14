# EnableFontSmooth

**分类:** 系统

**签名:** `long EnableFontSmooth()`

**描述:** 开启当前系统屏幕字体平滑.同时开启系统的ClearType功能.

## 参数

*此函数无参数。*

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
if dm.CheckFontSmooth()
= 0 then
if dm.EnableFontSmooth()
= 1 then
MessageBox "开启了当前系统平滑字体,重启生效"
dm.ExitOs 2
Delay 2000
EndScript
end if
end if
```

## 注意

- 开启之后要让系统生效，必须重启系统才有效.
