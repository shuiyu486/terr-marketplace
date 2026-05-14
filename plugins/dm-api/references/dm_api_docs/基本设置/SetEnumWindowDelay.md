# SetEnumWindowDelay

**分类:** 基本设置

**签名:** `long SetEnumWindowDelay(delay)`

**描述:** 设置EnumWindow  EnumWindowByProcess  EnumWindowSuper

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| delay | int | 单位毫秒 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.SetEnumWindowDelay
300000
```

## 注意

- 有些时候，窗口过多，并且窗口结构过于复杂，可能枚举的时间过长. 那么需要调用这个函数来延长时间。避免漏掉窗口.
