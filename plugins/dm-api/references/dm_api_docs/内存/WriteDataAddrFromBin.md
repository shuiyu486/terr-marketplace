函数简介:

对指定地址写入二进制数据,只不过直接从数据指针获取数据写入,不通过字符串. 适合高级用户.

函数原型:  
  
long WriteDataAddrFromBin(hwnd,addr,data,len)

参数定义:  
  
hwnd 整形数: 窗口句柄或者进程ID.  默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr长整形数: 地址

data 整形数: 数据指针  
len  整形数: 数据长度

返回值:

整形数:  
0 : 失败

1 : 成功

示例:

dm\_ret =
dm.WriteDataAddrFromBin(hwnd,2934793257239,1231234,10)

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。