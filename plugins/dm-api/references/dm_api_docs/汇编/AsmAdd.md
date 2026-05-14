# AsmAdd

**分类:** 汇编

**签名:** `long AsmAdd(asm_ins)`

**描述:** 添加指定的MASM汇编指令. 支持标准的masm汇编指令.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| asm_ins | str | MASM汇编指令,大小写均可以 比如 "mov eax,1" ,也支持直接加入字节，比如"emit 90 90 90 90"等. 同时也支持跳转指令，标记. 标记必须以":"开头. 跳转指令后必须接本次AsmCall之前的存在的有效Label. 另外跳转只支持短跳转,就是跳转的字节码不能超过128个字节. |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.AsmAdd "push 100"
dm.AsmAdd "push 60304d"
dm.AsmAdd "emit 90 90 90"
dm.AsmAdd "push dword ptr[112233bb]
dm.AsmAdd "call 678fed"

// 下面是一个跳转指令的例子
dm.AsmAdd "mov
eax,1"
dm.AsmAdd "cmp
eax,1"
dm.AsmAdd "je
Label1"
dm.AsmAdd "mov
eax,3"
dm.AsmAdd "jmp
Exit"
dm.AsmAdd ":Label1"
dm.AsmAdd "mov
eax,2"
dm.AsmAdd ":Exit"
dm.AsmCall hwnd,1
```

## 注意

- 有些人用老版本的插件，省略了dword qword word
- byte等前缀,事实上老版本语法规则不完善，容易出问题,从新版本7.1818开始，所有语法都必须是规范的masm语法.
- 大家可以参考od里的汇编语法.
- 以下的都是一些错误的写法
- push [112233bb]
- mov ecx,[aabbccdd]
- 等。 以下的才是正确的写法
- push dword ptr [112233bb]
- mov ecx,dword ptr[aabbccdd]
- mov cx,word ptr[aabbccdd]
- mov cl,byte ptr[aabbccdd]
