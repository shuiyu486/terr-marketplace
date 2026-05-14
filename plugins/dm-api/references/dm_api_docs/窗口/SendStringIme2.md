# SendStringIme2

**分类:** 窗口

**签名:** `long SendStringIme2(hwnd,str,mode)`

**描述:** 利用真实的输入法，对指定的窗口输入文字.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |
| str | str | 发送的文本数据 |
| mode | int | 取值意义如下: |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
If
dm.SendStringIme2(hwnd,"",200) = 1 then

dm.SendStringIme2 hwnd,"我是来测试的",0

dm.SendStringIme2 hwnd,"abc",0

dm.SendStringIme2 hwnd,"123",0

dm.SendStringIme2 hwnd,"",300
end if
```

## 注意

- 如果要同时对此窗口进行绑定，并且绑定的模式是1 3 5 7 101 103，那么您必须要在绑定之前,先执行加载输入法的操作. 否则会造成绑定失败!.
- 卸载时，没有限制.
- 还有，在后台输入时，如果目标窗口有判断是否在激活状态才接受输入文字,那么可以配合绑定窗口中的假激活属性来保证文字正常输入. 诸如此类. 基本上用这个没有输入不了的文字.
- BindWindow
- hwnd,"normal","normal","normal","dx.public.active.api|dx.public.active.message",0
- dm.SendStringIme2 hwnd,"哈哈",0
