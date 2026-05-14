函数简介:

搜索指定的二进制数据.

函数原型:  
  
string FindDataEx(hwnd, addr\_range, data,step,multi\_thread,mode)

参数定义:  
  
hwnd 整形数: 指定搜索的窗口句柄或者进程ID. 
默认是窗口句柄. 如果要指定为进程ID,需要调用[SetMemoryHwndAsProcessId](SetMemoryHwndAsProcessId.htm).

addr\_range 字符串: 指定搜索的地址集合，字符串类型，这个地方可以是上次FindXXX的返回地址集合,可以进行二次搜索.(类似CE的再次扫描)

            
如果要进行地址范围搜索，那么这个值为的形如如下(类似于CE的新搜索)

            "00400000-7FFFFFFF"
"80000000-BFFFFFFF" "00000000-FFFFFFFF" 等.

data 字符串: 要搜索的二进制数据 以字符串的形式描述
比如"00 01 23 45 67 86 ab ce f1"等  
            
这里也可以支持模糊查找,用??来代替单个字节. 比如"00 01 ?? ?? 67 86 ?? ce f1"等.  
            
注意,这里不支持半个字节,比如3?这种不行.

step 整形数: 搜索步长.

multi\_thread整形数:表示是否开启多线程查找.  0不开启，1开启.  
                  
开启多线程查找速度较快，但会耗费较多CPU资源.
不开启速度较慢，但节省CPU.

mode 整形数: 0: 略过内存类型为Mapped的内存,搜索可读可写可执行.  
           
 1: 略过内存类型为Mapped的内存,略过只读内存.  
        
   16: 全部内存类型,搜索可读可写可执行. (速度会很慢)  
           
17: 全部内存类型,略过只读内存. (速度会很慢)

返回值:

字符串:  
返回搜索到的地址集合，地址格式如下:

"addr1|addr2|addr3…|addrn"

比如"400050|423435|453430"  
  
如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.

示例:

// 全局搜索  
result = dm.FindDataEx(hwnd,"00000000-FFFFFFFF","00 01 23 45 67
86 ab ce f1",4,1,0)  
if len(result) = 0 then  
     MessageBox
"找不到"  
     EndScript  
end if  
  
result = split(result,"|")  
count = ubound(result)+1  
MessageBox "找到"&count&"个地址"

注: DmGuard中的memory护盾也可以突破部分窗口内存保护，可以尝试使用。