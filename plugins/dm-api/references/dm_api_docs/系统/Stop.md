# Stop

**分类:** 系统

**签名:** `long Stop(id)`

**描述:** 停止指定的音乐.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | Play返回的播放id. |

## 返回值

- 0 : 失败
- 1 : 成功.

## 示例

```vbs
// test.mp3放于d:\test目录下
dm.SetPath "d:\test"
id = dm.Play("test.mp3")

// 绝对路径
id = dm.Play("d:\test\test.mp3")
Delay 1000
dm.Stop id
```
