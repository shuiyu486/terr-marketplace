# DisablePowerSave

**分类:** 系统

**签名:** `long DisablePowerSave()`

**描述:** 关闭电源管理，不会进入睡眠.

## 参数

*此函数无参数。*

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm.DisablePowerSave

注 :此函数调用以后，并不会更改系统电源设置.
此函数经常用在后台操作过程中. 避免被系统干扰.
```
