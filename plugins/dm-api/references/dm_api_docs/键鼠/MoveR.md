# MoveR

**分类:** 键鼠

**签名:** `long MoveR(rx,ry)`

**描述:** 鼠标相对于上次的位置移动rx,ry.   如果您要使前台鼠标移动的距离和指定的rx,ry一致,最好配合[EnableMouseAccuracy](EnableMouseAccuracy.htm)函数来使用.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| rx | int | 相对于上次的X偏移 |
| ry | int | 相对于上次的Y偏移 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.MoveR rx,ry
```

## 注意

- 此函数从6.1550开始，为了兼容某些特殊输入，不再自动设置鼠标的速度和精确度。如果您要使前台鼠标移动的距离和指定的rx,ry一致,那么最好配合=EnableMouseAccuracy函数来使用
- 因为rx和ry的偏移量不一定就是鼠标真实的偏移,而是代表了物理鼠标DPI偏移. 如果您需要这个偏移和真实鼠标偏移一致，那么需要如下调用这个函数，如下所示:
- old\_accuracy = dm.EnableMouseAccuracy(0)
- // 关闭精确度开关
- dm.MoveR 30,30
- dm.EnableMouseAccuracy old\_accuracy
- 当然你也可以永久关闭精确度开关.  一般来说精确度开关默认都是关闭的.
- 以上这些设置都仅对前台有效. 后台是不需要这样设置的.
