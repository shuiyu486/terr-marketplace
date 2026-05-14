# FindWindowSuper

**分类:** 窗口

**签名:** `long FindWindowSuper(spec1,flag1,type1,spec2,flag2,type2)`

**描述:** 根据两组设定条件来查找指定窗口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| spec1 | str | 查找串1. (内容取决于flag1的值) |
| flag1 | int | 取值如下: |
| type1 | int | 取值如下 |
| spec2 | str | 查找串2. (内容取决于flag2的值) |
| flag2 | int | 取值如下: |
| type2 | int | 取值如下 |

## 返回值

- 整形数表示的窗口句柄，没找到返回0

## 示例

```vbs
hwnd = dm.FindWindowSuper("记事本",0,1,"notepad",1,0)
```
