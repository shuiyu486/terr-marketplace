# ReadFile

**分类:** 文件

**签名:** `string ReadFile(file)`

**描述:** 从指定的文件读取内容.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件 |

## 返回值

- 读入的文件内容

## 示例

```vbs
// 绝对路径
TracePrint dm.ReadFile("c:\123.txt")

// 相对路径
dm.SetPath "c:\test_game"
TracePrint dm.ReadFile("123.txt")
```
