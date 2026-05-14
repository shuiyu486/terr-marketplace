# Assemble

**分类:** 汇编

**签名:** `string Assemble(base_addr,is_64bit)`

**描述:** 把汇编缓冲区的指令转换为机器码 并用16进制字符串的形式输出

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| base_addr | long | 用AsmAdd添加到缓冲区的第一条指令所在的地址 |
| is_64bit | int | 表示缓冲区的指令是32位还是64位. 32位表示为0,64位表示为1 |

## 返回值

- 机器码，比如 "aa bb cc"这样的形式

## 示例

```vbs
code = dm.Assemble(&H405940,1)
MessageBox code
```
