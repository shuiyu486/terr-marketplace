# DeleteFile

**分类:** 文件

**签名:** `long DeleteFile(file)`

**描述:** 删除文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件名 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.DeleteFile "c:\123.txt"

// 相对路径
dm.SetPath "c:\test_game"
dm.DeleteFile "123.txt"
```
