# IsFileExist

**分类:** 文件

**签名:** `long IsFileExist(file)`

**描述:** 判断指定文件是否存在.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件名 |

## 返回值

- 0 : 不存在
- 1 : 存在

## 示例

```vbs
// 绝对路径
TracePrint dm.IsFileExist("c:\123.txt")

// 相对路径
dm.SetPath "c:\test_game"
TracePrint dm.IsFileExist("123.txt")
```
