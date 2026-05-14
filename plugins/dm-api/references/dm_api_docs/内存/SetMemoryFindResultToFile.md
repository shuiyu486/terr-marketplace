# SetMemoryFindResultToFile

**分类:** 内存

**签名:** `long SetMemoryFindResultToFile(file)`

**描述:** 设置是否把所有内存查找接口的结果保存入指定文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| file | str | 设置要保存的搜索结果文件名. 如果为空字符串表示取消此功能. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 开启
dm.SetPath "d:\test"
dm.SetMemoryFindResultToFile "result.dat"

//取消
dm.SetMemoryFindResultToFile ""
```

## 注意

- 部分高级语言无法接纳FindXXX 接口返回的超长字符串，那么需要用这个函数转存入文件,然后再读取分析处理.
- 同时，设置了此文件后，那么当下次调用FindXXX接口传入的地址参数时，并且地址参数不是范围参数,那么地址参数会从设置的文件中读取. 如果是范围参数,那么插件不会从设置的文件读取,会认为是首次查找.因为部分高级语言对参数的接收也有长度限制，无法接收超长字符串.
