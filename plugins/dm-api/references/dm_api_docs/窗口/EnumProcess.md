# EnumProcess

**分类:** 窗口

**签名:** `string EnumProcess(name)`

**描述:** 根据指定进程名,枚举系统中符合条件的进程PID,并且按照进程打开顺序排序.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| name | str | 进程名,比如qq.exe |

## 返回值

- 字符串 : 返回所有匹配的进程PID,并按打开顺序排序,格式"pid1,pid2,pid3"

## 示例

```vbs
pids = dm.EnumProcess("notepad.exe")
pids = split(pids,",")

转换为数组后,就可以处理了

这里注意, pids数组里的是字符串,要用于使用,还得强制类型转换,比如clng(pids(0))
```
