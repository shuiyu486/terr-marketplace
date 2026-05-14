# HackSpeed

**分类:** 后台设置

**签名:** `long HackSpeed(rate)`

**描述:** 对目标窗口设置加速功能(类似变速齿轮),必须在绑定参数中有dx.public.hack.speed时才会生效.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| rate | double | 取值范围大于0. 默认是1.0 表示不加速，也不减速. 小于1.0表示减速,大于1.0表示加速. 精度为小数点后1位. 也就是说1.5 和 1.56其实是一样的. |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindowEx(hwnd,"normal","normal","normal","dx.public.hack.speed",0)
// 2倍加速
dm.HackSpeed 2.0

// 2.5倍
dm.HackSpeed 2.5

// 10.1倍
dm.HackSpeed 10.1

// 速度降低为原来的一半
dm.HackSpeed 0.5

// 速度降低为原来的十分之一
dm.HackSpeed 0.1
```

## 注意

- 此接口必须在绑定窗口成功以后调用，而且必须有参数dx.public.hack.speed. 不一定对所有窗口有效,具体自己测试.
