# DeleteIniPwd

**分类:** 文件

**签名:** `long DeleteIniPwd(section,key,file,pwd)`

**描述:** 删除指定的ini小节.支持加密文件

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. 如果这个变量为空串，则删除整个section小节. |
| file | str | ini文件名. |
| pwd | str | 密码. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.DeleteIniPwd
"Global","var1","c:\test_game\cfg.ini","1234"

// 相对路径
dm.SetPath "c:\test_game"
dm.DeleteIniPwd
"Global","","cfg.ini","1234"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱. 但是多进程是不安全的,要避免多进程同时使用此接口,否则会造成数据错乱.

如果此文件没加密，调用此函数会自动加密.
```
