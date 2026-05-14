# WriteFile

**分类:** 文件

**签名:** `long WriteFile(file,content)`

**描述:** 向指定文件追加字符串.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件 |
| content | str | 写入的字符串. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.WriteFile "c:\123.txt","哈哈哈"

// 相对路径
dm.SetPath "c:\test_game"
dm.WriteFile "123.txt","哈哈哈"
```
