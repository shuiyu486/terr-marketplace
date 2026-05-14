# IsFolderExist

**分类:** 文件

**签名:** `long IsFolderExist (folder)`

**描述:** 判断指定目录是否存在.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| folder | str | 目录名 |

## 返回值

- 0 : 不存在
- 1 : 存在

## 示例

```vbs
TracePrint dm.IsFolderExist("c:\test_game")
```
