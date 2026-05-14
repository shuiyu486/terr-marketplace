# MoveFile

**分类:** 文件

**签名:** `long MoveFile(src_file,dst_file)`

**描述:** 移动文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| src_file | str | 原始文件名 |
| dst_file | str | 目标文件名. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.MoveFile "c:\123.txt","d:\456.txt"

// 相对路径
dm.SetPath "c:\test_game"
dm.MoveFile "123.txt","456.txt"
```
