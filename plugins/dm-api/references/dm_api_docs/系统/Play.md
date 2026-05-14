# Play

**分类:** 系统

**签名:** `long Play(media_file)`

**描述:** 播放指定的MP3或者wav文件.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| media_file | str | 指定的音乐文件，可以采用文件名或者绝对路径的形式. |

## 返回值

- 0 : 失败 非0表示当前播放的ID。可以用Stop来控制播放结束.

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
