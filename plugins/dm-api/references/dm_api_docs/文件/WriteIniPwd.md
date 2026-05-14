# WriteIniPwd

**分类:** 文件

**签名:** `long WriteIniPwd(section,key,value,file,pwd)`

**描述:** 向指定的Ini写入信息.支持加密文件

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. |
| value | str | 变量内容 |
| file | str | ini文件名. |
| pwd | str | 密码. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.WriteIniPwd
"Global","var1","123","c:\test_game\cfg.ini","1234"

// 相对路径
dm.SetPath "c:\test_game"
dm.WriteIniPwd
"Global","var1","123","cfg.ini","1234"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果此文件没加密，调用此函数会自动加密.
```
