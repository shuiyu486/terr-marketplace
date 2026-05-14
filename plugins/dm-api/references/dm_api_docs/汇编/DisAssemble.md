# DisAssemble

**分类:** 汇编

**签名:** `string DisAssemble(asm_code,base_addr, is_64bit)`

**描述:** 把指定的机器码转换为汇编语言输出

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| asm_code | str | 机器码，形式如 "aa bb cc"这样的16进制表示的字符串(空格无所谓) |
| base_addr | long | 指令所在的地址 |
| is_64bit | int | 表示asm_code表示的指令是32位还是64位. 32位表示为0,64位表示为1 |

## 返回值

- MASM汇编语言字符串.如果有多条指令，则每条指令以字符"|"连接.

## 示例

```vbs
dm_ret = dm.DisAssemble("81 05 E0 5A
47 00 01 00 00 00",&H435fde,0)
MessageBox dm_ret
```
