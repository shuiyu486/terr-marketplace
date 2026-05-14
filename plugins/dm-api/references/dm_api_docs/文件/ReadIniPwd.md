# ReadIniPwd

**分类:** 文件

**签名:** `string ReadIniPwd(section,key,file,pwd)`

**描述:** 从Ini中读取指定信息.可支持加密文件

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. |
| file | str | ini文件名. |
| pwd | str | 密码 |

## 返回值

- 字符串形式表达的读取到的内容

## 示例

```vbs
// 绝对路径
Text = dm.ReadIniPwd("Global","var1","c:\test_game\cfg.ini","1234")

// 相对路径
dm.SetPath "c:\test_game"
Text = dm.ReadIniPwd("Global","var1","cfg.ini","1234")

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果文件没加密，也可以正常读取.
```
