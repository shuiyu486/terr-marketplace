# DmGuardExtract

**分类:** 防护盾

**签名:** `long DmGuardExtract(type,path)`

**描述:** 释放插件用的驱动. 可以自己拿去签名. 防止有人对我的签名进行检测. 强烈推荐使用驱动的用户使用. 仅释放64位系统的驱动.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| type | str | 需要释放的驱动类型. 这里写"common"即可. |
| path | str | 释放出的驱动文件全路径. 比如"c:\test.sys". |

## 返回值

- 0 : 不支持的type
- 1 : 成功
- -2: 释放失败

## 示例

```vbs
dm.DmGuardExtract "common","c:\test.sys"

注 : 释放出的文件进行签名后,可以再用DmGuardLoadCustom来进行加载.
```
