# VirtualQueryEx

**分类:** 内存

**签名:** `string VirtualQueryEx(hwnd,addr,pmbi)`

**描述:** 获取指定窗口，指定地址的内存属性.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm). |
| addr | long | 需要查询的地址 pmbi **整形数**: 这是一个地址,指向的内容是MEMORY_BASIC_INFORMATION32或者MEMORY_BASIC_INFORMATION64. 取决于要查询的进程是32位还是64位. 这个地址可以为0,忽略这个参数. 下面是这2个结构体在vc下的定义: typedef struct _MEMORY_BASIC_INFORMATION32 { DWORD BaseAddress; DWORD AllocationBase; DWORD AllocationProtect; DWORD RegionSize; DWORD State; DWORD Protect; DWORD Type; } MEMORY_BASIC_INFORMATION32, \*PMEMORY_BASIC_INFORMATION32; typedef struct DECLSPEC_ALIGN(16) _MEMORY_BASIC_INFORMATION64 { ULONGLONG BaseAddress; ULONGLONG AllocationBase; DWORD     AllocationProtect; DWORD     __alignment1; ULONGLONG RegionSize; DWORD     State; DWORD     Protect; DWORD     Type; DWORD     __alignment2; } MEMORY_BASIC_INFORMATION64, \*PMEMORY_BASIC_INFORMATION64; |

## 返回值

- 查询的结果以字符串形式.  内容是"BaseAddress,AllocationBase,AllocationProtect,RegionSize,State,Protect,Type" 数值都是10进制表达.

## 示例

```vbs
这里我们给一个VC的例子. 其它语言都差不多.
MEMORY_BASIC_INFORMATION32 mbi
= {0};
dm->VirtualQueryEx(hwnd,0x400000,&mbi);
if (mbi.BaseAddress)
{
// 做一些你需要的操作
}
```

## 注意

- 如果正常方式无法修改内存的读写属性,可以尝试配合DmGuard中的memory护盾,突破部分窗口内存保护。
