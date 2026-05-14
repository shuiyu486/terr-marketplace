函数简介:

读取指定地址的字符串，可以是GBK字符串或者是Unicode字符串.(必须事先知道内存区的字符串编码方式)

函数原型:  
  
string ReadString(hwnd,addr,type,len)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr 字符串: 用字符串来描述地址，类似于CE的地址描述，数值必须是16进制,里面可以用[ ] + -这些符号来描述一个地址。+表示地址加，-表示地址减  
       模块名必须用<>符号来圈起来

      例如:

1.        
"4DA678"
最简单的方式，用绝对数值来表示地址

2.        
"<360SE.exe>+DA678"
相对简单的方式，只是这里用模块名来决定模块基址，后面的是偏移

3.        
"[4DA678]+3A" 用绝对数值加偏移，相当于一级指针

4.        
"[<360SE.exe>+DA678]+3A" 用模块定基址的方式，也是一级指针

5.        
"[[[<360SE.exe>+DA678]+3A]+5B]+8" 这个是一个三级指针

总之熟悉CE的人 应该对这个地址描述都很熟悉,我就不多举例了

type 整形数: 字符串类型,取值如下

      0 : GBK字符串

      1 : Unicode字符串

      2 : UTF8字符串

len 整形数: 需要读取的字节数目.如果为0，则自动判定字符串长度.

返回值:

字符串:  
读取到的字符串  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

value =
dm.ReadString(hwnd,"4DA678",0,0)  
MessageBox  value

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。