# DecodeFile

**分类:** 文件

**签名:** `long DecodeFile(file,pwd)`

**描述:** 解密指定的文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 文件名. |
| pwd | str | 密码. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.DecodeFile "c:\test_game\cfg.ini","1234"

// 相对路径
dm.SetPath "c:\test_game"
dm.DecodeFile "1.bmp","1234"

如果此文件没加密，调用此函数不会有任何效果.
插件所有的字库 图片 ini都是用此接口来解密.
```
