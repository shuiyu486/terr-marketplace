# GetCpuType

**分类:** 系统

**签名:** `long GetCpuType()`

**描述:** 获取当前CPU类型(intel或者amd).

## 参数

*此函数无参数。*

## 返回值

- 0 : 未知
- 1 : Intel cpu
- 2 : AMD cpu

## 示例

```vbs
if dm.GetCpuType() <> 1 then
MessageBox "当前系统CPU不是intel
cpu,不支持!"
EndScript
end if
```
