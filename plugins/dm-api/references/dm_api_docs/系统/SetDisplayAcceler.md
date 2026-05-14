# SetDisplayAcceler

**分类:** 系统

**签名:** `long SetDisplayAcceler(level)`

**描述:** 设置当前系统的硬件加速级别.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| level | int | 取值范围为0-5.  0表示关闭硬件加速。5表示完全打开硬件加速. |

## 返回值

- 0 : 失败.
- 1 : 成功.

## 示例

```vbs
// 关闭硬件加速
TracePrint SetDisplayAcceler(0)
```

## 注意

- 此函数只在XP 2003系统有效.
