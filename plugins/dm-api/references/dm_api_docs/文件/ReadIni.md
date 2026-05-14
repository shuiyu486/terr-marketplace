# ReadIni

**分类:** 文件

**签名:** `string ReadIni(section,key,file)`

**描述:** 从Ini中读取指定信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. |
| file | str | ini文件名. |

## 返回值

- 字符串形式表达的读取到的内容

## 示例

```vbs
// 绝对路径
Text =
dm.ReadIni("Global","var1","c:\test_game\cfg.ini")

// 相对路径
dm.SetPath "c:\test_game"
Text = dm.ReadIni("Global","var1","cfg.ini")

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.
```
