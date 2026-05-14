# DownloadFile

**分类:** 文件

**签名:** `long DownloadFile(url,save_file,timeout)`

**描述:** 从internet上下载一个文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| url | str | 下载的url地址. |
| save_file | str | 要保存的文件名. |
| timeout | int | 连接超时时间，单位是毫秒. |

## 返回值

- 1 : 成功
- -1 : 网络连接失败
- -2 : 写入文件失败

## 示例

```vbs
dm.DownloadFile "www.sohu.com","sohu.html",3000

dm.DownloadFile "http://www.sohu.com","d:\sohu.html",3000
```
