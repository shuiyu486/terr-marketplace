# RunApp

**分类:** 系统

**签名:** `long RunApp(app_path,mode)`

**描述:** 运行指定的应用程序.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| app_path | str | 指定的可执行程序全路径. |
| mode | int | 取值如下 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm.RunApp "c:\windows\notepad.exe",0

dm.RunApp "notepad",1
```
