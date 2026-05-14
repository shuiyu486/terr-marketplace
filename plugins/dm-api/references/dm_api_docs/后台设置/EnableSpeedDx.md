# EnableSpeedDx

**分类:** 后台设置

**签名:** `long EnableSpeedDx(enable)`

**描述:** 设置是否开启高速dx键鼠模式。 默认是关闭.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.EnableSpeedDx 1
```

## 注意

- 此函数开启的后果就是，所有dx键鼠操作将不会等待，适用于某些特殊的场合(比如避免窗口无响应导致宿主进程也卡死的问题).
- EnableMouseSync和EnableKeyboardSync开启以后，此函数就无效了.
- 此函数可能在部分窗口下会有副作用，谨慎使用!!
