# SetSendStringDelay

**分类:** 窗口

**签名:** `long SetSendStringDelay(delay)`

**描述:** 设置SendString和SendString2的每个字符之间的发送间隔.  有些窗口必须设置延迟才可以正常发送. 否则可能会顺序错乱.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| delay | int | 大于等于0的延迟数值. 单位是毫秒. 默认是0 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm.SetSendStringDelay 100
dm.SendString hwnd,"abcd"
```
