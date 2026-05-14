# CheckInputMethod

**分类:** 杂项

**签名:** `long CheckInputMethod(hwnd,input_method)`

**描述:** 检测指定窗口所在线程输入法是否开启

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄 |
| input_method | str | 输入法名字。 具体输入法名字对应表查看注册表中以下位置: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts 下面的每一项下的Layout Text的值就是输入法名字 比如 "中文 - QQ拼音输入法" 以此类推. |

## 返回值

- 0 : 未开启
- 1 : 开启

## 示例

```vbs
dm_ret = dm.CheckInputMethod(hwnd,"中文 - QQ拼音输入法")
if dm_ret = 1 then
msgbox "QQ输入法开启拉"
end if
```
