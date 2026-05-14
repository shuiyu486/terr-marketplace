# SendStringIme

**分类:** 窗口

**签名:** `long SendStringIme(str)`

**描述:** 向绑定的窗口发送文本数据.必须配合dx.public.input.ime属性.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| str | str | 发送的文本数据 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindowEx(hwnd,"normal","normal","normal","dx.public.input.ime",0)
dm.SendStringIme "我是来测试的"
```
