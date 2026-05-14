# GetFileLength

**分类:** 文件

**签名:** `long GetFileLength(file)`

**描述:** 获取指定的文件长度.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件名 |

## 返回值

- 文件长度(字节数)

## 示例

```vbs
// 绝对路径
TracePrint dm.GetFileLength("c:\123.txt")

// 相对路径
dm.SetPath "c:\test_game"
TracePrint dm.GetFileLength("123.txt")
```
