# GetTime

**分类:** 系统

**签名:** `long GetTime()`

**描述:** 获取当前系统从开机到现在所经历过的时间，单位是毫秒

## 参数

*此函数无参数。*

## 返回值

- 时间(单位毫秒)

## 示例

```vbs
t1 = dm.GetTime()
dm_ret = dm.FindPic(0,0,2000,2000,"test.bmp","000000",1.0,0,x,y)
t2 = dm.GetTime()
MessageBox (t2-t1)
```
