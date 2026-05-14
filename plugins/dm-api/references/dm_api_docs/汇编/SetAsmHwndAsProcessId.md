# SetAsmHwndAsProcessId

**分类:** 汇编

**签名:** `long SetAsmHwndAsProcessId(enable)`

**描述:** 使用AsmCall时的hwnd参数当作进程pid. 注:仅对AsmCall的模式1起作用,因为其它模式都需要窗口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0关闭,1打开 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.SetAsmHwndAsProcessId 1
dm.AsmCall pid,1
```
