函数简介:

执行用AsmAdd加到缓冲中的指令.  这个接口同AsmCall,但是由于插件内部在每次AsmCall时,都会有对目标进程分配内存的操作,这样会不够效率.  
所以增加这个接口，可以让调用者指定分配好的内存,并在此内存上执行call的操作.

函数原型:  
  
LONGLONG AsmCallEx(hwnd,mode,base\_addr)

参数定义:  
  
hwnd 整形数: 窗口句柄

mode 整形数: 模式，取值如下

       0 : 在本进程中进行执行，这时hwnd无效. 注: 此模式会创建线程.

       1 : 对hwnd指定的进程内执行,注入模式为创建远程线程

       2 ：必须在对目标窗口进行注入绑定后,才可以用此模式(直接在目标进程创建线程).此模式下的call的执行是排队的,如果同时有多个call在此窗口执行,那么必须排队.所以执行效率不如模式1.
同时此模式受目标窗口刷新速度的影响,目标窗口刷新太慢，也会影响此模式的速度. 注: 此模式会创建线程.

       3 ：同模式2,但是此模式不会创建线程,而直接在hwnd所在线程执行.

       4 ：同模式0, 但是此模式不会创建线程,直接在当前调用AsmCall的线程内执行.  
  
    5 : 对hwnd指定的进程内执行,注入模式为APC.
此模式必须开启memory盾。任意一个memory盾都可以.  
  
    6 : 直接hwnd所在线程执行.

base\_addr字符串**:** 16进制格式. 比如"45A00000",此参数指定的地址必须要求有可读可写可执行属性. 并且内存大小最少要200个字节. 模式6要求至少400个字节. 如果Call的内容较多,那么长度相应也要增加.   如果此参数为空,那么效果就和AsmCall一样.

返回值:

长整形数:  
获取执行汇编代码以后的EAX的值(32位进程),或者RAX的值(64位进程).一般是函数的返回值. 如果要想知道函数是否执行成功，请查看[GetLastError](../基本设置/GetLastError.htm)函数.  
-200 : 执行中出现错误.  
-201 : 使用模式5时，没有开启memory盾.

示例:

base\_addr =
dm.VirtualAllocEx(hwnd,0,200,0)  
dm.AsmClear  
dm.AsmAdd "mov eax,1"  
dm.AsmAdd "push 0123456"  
dm.AsmAdd "call 0343434"  
dm.AsmCallEx hwnd,1,hex(base\_addr)

另要注意的是，AsmAdd里所有的数值都是16进制.

注: 有些时候有保护的时候，此函数执行会失败，那么此时可以尝试用memory保护盾来试试看.

这里特别对64位的汇编执行做一个简单的说明. 因为64位寻址的限制,那么类似下面的call可能会无法正确寻址.  
call 1234aabbccdd  
因为call 绝对地址只能寻址上下2G的范围,超过以后就无法寻址. 所以类似这样的语句，我们要改为下面的方式,比如  
mov rax,1234aabbccdd  
call rax  
  
另外，由于64位调用的约定,前4个参数通过rcx rdx r8 r9来传递,后面的参数通过栈来传递,同时要给call预留28h字节的栈空间.  
比如上面的call正确的写法如下:  
mov rax,1234aabbccdd  
sub rsp,28  
call rax  
add rsp,28  
  
也就说，所有的call前后，一定得有sub rsp,28和add rsp,28

如果要传递超过4个参数，则按照从右往左的顺序压栈. 具体以MoveWindow这个接口为例.  
BOOL WINAPI MoveWindow( \_\_in HWND hWnd, \_\_in int X, \_\_in int Y, \_\_in int
nWidth, \_\_in int nHeight, \_\_in BOOL bRepaint)  
MoveWindow这个API是6个参数,由于多了2个参数，所以这里的sub
rsp,28也要改变，每个参数多8个字节(无论参数是不是8个字节). 也就是这里变成sub
rsp,38  
另外要注意,push的参数必须从10h开始push.具体原因我也不知道. 看这里的例子  
mov rcx, hWnd   这里传入第一个参数hWnd  
mov rdx, X      这里传入第二个参数X  
mov r8d, Y      这里传入第三个参数Y  
mov r9d, nWidth 这里传入第四个参数nWidth  
mov r11,rsp 保存原始的rsp,方便后面传递参数  
sub rsp,38  
mov dword ptr[r11-10],bRepaint 这里传入第六个参数.(从右往左)  
mov dword ptr[r11-18],nHeight  这里传入第五个参数.  
call MoveWindow  
add rsp,38  
  
完整的测试代码如下(必须是64位的顶级窗口)  
set dm = CreateObject("dm.dmsoft")  
hwnd = dm.GetMousePointWindow()  
user32\_base = dm.GetModuleBaseAddr(hwnd,"user32.dll")  
MoveWindow\_addr =
dm.GetRemoteApiAddress(hwnd,user32\_base,"MoveWindow")

if dm.GetWindowState(hwnd,9)
= 1 then  
   dm.AsmClear  
   dm.AsmAdd "mov
rcx," & hex(hwnd)  
   dm.AsmAdd "mov
rdx," & hex(0)  
   dm.AsmAdd "mov
r8," & hex(0)  
   dm.AsmAdd "mov r9,"
& hex(300)  
   dm.AsmAdd "mov
r11,rsp"  
   dm.AsmAdd "sub
rsp,38"  
   dm.AsmAdd "mov dword
ptr[r11-10]," & hex(1)  
   dm.AsmAdd "mov dword
ptr[r11-18]," & hex(400)  
   dm.AsmAdd "mov
rax," & hex(MoveWindow\_addr)  
   dm.AsmAdd "call
rax"  
   dm.AsmAdd "add
rsp,38"  
end if

dm.AsmCall hwnd,1