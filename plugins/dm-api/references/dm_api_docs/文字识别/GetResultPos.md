# GetResultPos

**分类:** 文字识别

**签名:** `long GetResultPos(ret,index,intX,intY)`

**描述:** 对插件部分接口的返回值进行解析,并根据指定的第index个坐标,返回具体的值

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| ret | str | 部分接口的返回串 |
| index | int | 第几个坐标 |
| intX | int* | 返回X坐标 |
| intY | int* | 返回Y坐标 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
s =
dm.FindColorEx(0,0,2000,2000,"123456-000000|abcdef-202020",1.0,0)
count = dm.GetResultCount(s)
index = 0
Do While index < count
dm_ret = dm.GetResultPos(s,index,intX,intY)
MessageBox
intX&","&intY
index = index + 1
Loop
```
