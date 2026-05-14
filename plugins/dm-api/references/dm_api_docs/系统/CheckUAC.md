# CheckUAC

**分类:** 系统

**签名:** `long CheckUAC()`

**描述:** 检测当前系统是否有开启UAC(用户账户控制).

## 参数

*此函数无参数。*

## 返回值

- 0 : 没开启UAC
- 1 : 开启了UAC

## 示例

```vbs
if dm.CheckUAC() = 1 then
TracePrint "当前系统开启了用户账户控制"
end if
```

## 注意

- 只有WIN7 WIN8 VISTA WIN2008以及以上系统才有UAC设置
