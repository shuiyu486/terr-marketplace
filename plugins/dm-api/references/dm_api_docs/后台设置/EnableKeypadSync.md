# EnableKeypadSync

**分类:** 后台设置

**签名:** `long EnableKeypadSync(enable,time_out)`

**描述:** 键盘消息采用同步发送模式.默认异步.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 禁止同步 |
| time_out | int | 单位是毫秒,表示同步等待的最大时间. |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)
dm.EnableKeypadSync 1,200
```

## 注意

- 此接口必须在绑定之后才能调用。
- 有些时候，如果是异步发送，如果发送动作太快,中间没有延时,有可能下个动作会影响前面的.
- 而用同步就没有这个担心.
