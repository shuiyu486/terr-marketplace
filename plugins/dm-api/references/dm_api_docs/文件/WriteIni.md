# WriteIni

**分类:** 文件

**签名:** `long WriteIni(section,key,value,file)`

**描述:** 向指定的Ini写入信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. |
| value | str | 变量内容 |
| file | str | ini文件名. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.WriteIni
"Global","var1","123","c:\test_game\cfg.ini"

// 相对路径
dm.SetPath "c:\test_game"
dm.WriteIni
"Global","var1","123","cfg.ini"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.
```
