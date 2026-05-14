# Is64Bit

**分类:** 系统

**签名:** `long Is64Bit()`

**描述:** 判断当前系统是否是64位操作系统

## 参数

*此函数无参数。*

## 返回值

- 0 : 不是64位系统
- 1 : 是64位系统

## 示例

```vbs
if dm.Is64Bit() = 1 then
MessageBox "64位系统"
else
MessageBox "不是64位系统"
end if
```
