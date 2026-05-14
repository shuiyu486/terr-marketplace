# GetRemoteApiAddress

**分类:** 内存

**签名:** `LONGLONG GetRemoteApiAddress(hwnd,base_addr,fun_name)`

**描述:** 根据指定的目标模块地址,获取目标窗口(进程)内的导出函数地址.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| base_addr | long | 目标模块地址,比如user32.dll的地址,可以通过GetModuleBaseAddr来获取. |
| fun_addr | str | **:**需要获取的导出函数名. 比如"SetWindowTextA". |

## 返回值

- 获取的地址. 如果失败返回0

## 示例

```vbs
// 此例子用来在目标进程内执行SetWindowTextA来更改窗口标题.
hwnd = dm.GetMousePointWindow()
user32_base = dm.GetModuleBaseAddr(hwnd,"user32.dll")
SetWindowTextA_addr =
dm.GetRemoteApiAddress(hwnd,user32_base,"SetWindowTextA")

addr = dm.VirtualAllocEx(hwnd,0,50,0)
dm.WriteStringAddr hwnd,addr,0,"哈哈"

// 64位和32位的汇编代码不同
if dm.GetWindowState(hwnd,9) = 0 then
dm.AsmClear
dm.AsmAdd "mov
eax," & hex(addr)
dm.AsmAdd "push
eax"
dm.AsmAdd "mov
eax," & hex(hwnd)
dm.AsmAdd "push
eax"
dm.AsmAdd "call
" & hex(SetWindowTextA_addr)
else
dm.AsmClear
dm.AsmAdd "mov
rcx," & dm.Hex64(hwnd)
dm.AsmAdd "mov
rdx," & dm.Hex64(addr)
dm.AsmAdd "mov
rax," & dm.Hex64(SetWindowTextA_addr)
dm.AsmAdd "sub
rsp,28"
dm.AsmAdd "call
rax"
dm.AsmAdd "add
rsp,28"
end if

dm.AsmCall hwnd,1
dm.VirtualFreeEx hwnd,addr
```
