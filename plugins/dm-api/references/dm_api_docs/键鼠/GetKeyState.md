# GetKeyState

**分类:** 键鼠

**签名:** `long GetKeyState(vk_code)`

**描述:** 获取指定的按键状态.(前台信息,不是后台)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| vk_code | int | 虚拟按键码 |

## 返回值

- 0:弹起
- 1:按下

## 示例

```vbs
TracePrint dm.GetKeyState(13)
```
