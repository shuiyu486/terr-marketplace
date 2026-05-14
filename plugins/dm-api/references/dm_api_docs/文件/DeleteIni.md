# DeleteIni

**分类:** 文件

**签名:** `long DeleteIni(section,key,file)`

**描述:** 删除指定的ini小节.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| section | str | 小节名 |
| key | str | 变量名. 如果这个变量为空串，则删除整个section小节. |
| file | str | ini文件名. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 绝对路径
dm.DeleteIni "Global","var1" ,"c:\test_game\cfg.ini"

// 相对路径
dm.SetPath "c:\test_game"
dm.DeleteIni "Global","" ,"cfg.ini"

注 : 此函数是多线程安全的. 多线程同时读写同个文件不会造成文件错乱.
```
