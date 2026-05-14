# GetCursorSpot

**分类:** 键鼠

**签名:** `string GetCursorSpot()`

**描述:** 获取鼠标热点位置.(参考工具中抓取鼠标后，那个闪动的点就是热点坐标,不是鼠标坐标)

## 参数

*此函数无参数。*

## 返回值

- 成功时，返回形如"x,y"的字符串 失败时，返回空的串.

## 示例

```vbs
hot_pos = dm.GetCursorSpot()
if len(hot_pos) > 0 Then
hot_pos
= split(hot_pos,",")
x = int(hot_pos(0))
y = int(hot_pos(1))
end if
```
