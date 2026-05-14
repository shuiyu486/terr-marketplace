# GetOsBuildNumber

**分类:** 系统

**签名:** `long GetOsBuildNumber()`

**描述:** 得到操作系统的build版本号.  比如win10 16299,那么返回的就是16299. 其他类似

## 参数

*此函数无参数。*

## 返回值

- build 版本号 失败返回0

## 示例

```vbs
os_build_number = dm.GetOsBuildNumber()

WIN11的BuildNumber从22000开始. 如果要判断是不是WIN11,直接判断BuildNumber是否大于等于22000即可.
```
