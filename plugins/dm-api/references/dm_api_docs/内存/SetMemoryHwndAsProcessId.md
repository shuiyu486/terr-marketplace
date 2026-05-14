# SetMemoryHwndAsProcessId

**分类:** 内存

**签名:** `long SetMemoryHwndAsProcessId(en)`

**描述:** 设置是否把所有内存接口函数中的窗口句柄当作进程ID,以支持直接以进程ID来使用内存接口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| en | int | 取值如下 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm.SetMemoryHwndAsProcessId 1
```

## 注意

- 默认是当作窗口句柄.
