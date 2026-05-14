# EnableKeypadPatch

**分类:** 后台设置

**签名:** `long EnableKeypadPatch(enable)`

**描述:** 键盘消息发送补丁. 默认是关闭.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 禁止 |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)
dm.EnableKeypadPatch 1
```

## 注意

- 此接口必须在绑定之后才能调用。
