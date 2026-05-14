函数简介:

读取指定地址的二进制数据

函数原型:  
  
string ReadDataAddr(hwnd,addr,len)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

len 整形数: 二进制数据的长度

返回值:

字符串:  
读取到的数值,以16进制表示的字符串 每个字节以空格相隔 比如"12 34 56 78 ab
cd ef"  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

value =
dm.ReadDataAddr(hwnd,123456,10)  
MessageBox  value

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。  
如果要读取的数据长度过长，比如几十K的数据，由于COM组件的限制，可能无法返回如此长的字符串. 解决办法是分批读取.