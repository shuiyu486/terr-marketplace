# EnumIniKey

**分类:** 文件

**签名:** `string EnumIniKey(section,file)`

**描述:** 根据指定的ini文件以及section,枚举此section中所有的key名

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名. (不可为空) |
| file | str | ini文件名. |

## 返回值

- 每个key用"|"来连接，如果没有key，则返回空字符串. 比如"aaa|bbb|ccc"

## 示例

```vbs
// 绝对路径
dm_ret = dm.EnumIniKey("aaa","c:\test_game\cfg.ini")

// 相对路径
dm.SetPath "c:\test_game"
dm_ret = dm.EnumIniKey("aaa","cfg.ini")

if len(dm_ret) > 0 then
keys = split(dm_ret,"|")
count = ubound(keys) + 1
index = 0
Do While index < count
TracePrint
keys(index)
index = index +
1
Loop

end if

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.
另外,此函数无法枚举没有section的key.
```
