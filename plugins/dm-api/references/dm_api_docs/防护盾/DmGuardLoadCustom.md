# DmGuardLoadCustom

**分类:** 防护盾

**签名:** `long DmGuardLoadCustom(type,path)`

**描述:** 加载用DmGuardExtract释放出的驱动. 建议自己签名后,然后找个自己喜欢的路径加载. 仅支持64位系统的驱动加载.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| type | str | 需要释放的驱动类型. 这里写"common"即可. |
| path | str | 驱动文件全路径. 比如"c:\test.sys". |

## 返回值

- 返回值请参考DmGuard的返回值. 一样的含义.

## 示例

```vbs
dm.DmGuardLoadCustom "common","c:\test.sys"

注 : 这个路径只是演示. 实际上最好不要放在这么随意的位置. 一般驱动文件都在c:\windows\system32目录下.
```
