# EnableRealKeypad

**分类:** 后台设置

**签名:** `long EnableRealKeypad(enable)`

**描述:** 键盘动作模拟真实操作,点击延时随机.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭模拟 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.EnableRealKeypad 1

dm.KeyPressChar "E"
```

## 注意

- 此接口对KeyPress KeyPressChar KeyPressStr起作用。具体表现是键盘按下和弹起的间隔会在
- 当前设定延时的基础上,上下随机浮动50%. 假如
- 设定的键盘延时是100,那么这个延时可能就是50-150之间的一个值.
- 设定延时的函数是 SetKeypadDelay
