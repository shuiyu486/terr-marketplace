# EnableRealMouse

**分类:** 后台设置

**签名:** `long EnableRealMouse(enable,mousedelay,mousestep)`

**描述:** 鼠标动作模拟真实操作,带移动轨迹,以及点击延时随机.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭模拟 |
| mousedelay | int | 单位是毫秒. 表示在模拟鼠标移动轨迹时,每移动一次的时间间隔.这个值越大,鼠标移动越慢. 必须大于0,否则会失败. |
| Mousestep | int | 表示在模拟鼠标移动轨迹时,每移动一次的距离. 这个值越大，鼠标移动越快速. |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.EnableRealMouse 1,20,30

dm.MoveTo 100,100
dm.MoveTo 500,500
```

## 注意

- 此接口同样对LeftClick RightClick MiddleClick LeftDoubleClick起作用。具体表现是鼠标按下和弹起的间隔会在
- 当前设定延时的基础上,上下随机浮动50%. 假如
- 设定的鼠标延时是100,那么这个延时可能就是50-150之间的一个值.
- 设定延时的函数是
- SetMouseDelay
