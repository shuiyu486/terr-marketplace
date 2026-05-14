# FindWindowByProcess

**分类:** 窗口

**签名:** `long FindWindowByProcess(process_name,class,title)`

**描述:** 根据指定的进程名字，来查找可见窗口.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| process_name | str | 进程名. 比如(notepad.exe).这里是精确匹配,但不区分大小写. |
| class | str | 窗口类名，如果为空，则匹配所有. 这里的匹配是模糊匹配. |
| title | str | 窗口标题,如果为空，则匹配所有.这里的匹配是模糊匹配. |

## 返回值

- 整形数表示的窗口句柄，没找到返回0

## 示例

```vbs
hwnd = dm.FindWindowByProcess("noteapd.exe","","记事本")
```
