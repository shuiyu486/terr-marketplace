函数简介:

设置当前对象用于输入的对象. 结合图色对象和键鼠对象,用一个对象完成操作.

函数原型:  
  
long SetInputDm(dm\_id,rx,ry)

参数定义:

dm\_id
整形数: 接口GetId的返回值  
rx 整形数: 两个对象绑定的窗口的左上角坐标的x偏移. 是用dm\_id对应的窗口的左上角x坐标减去当前窗口左上角坐标的x坐标. 一般是0  
ry 整形数: 两个对象绑定的窗口的左上角坐标的y偏移. 是用dm\_id对应的窗口的左上角y坐标减去当前窗口左上角坐标的y坐标. 一般是0

返回值:

整形数:  
0: 失败  
1: 成功

示例:

// 创建2个对象  
set dm = createobject("dm.dmsoft")  
set dm2 = createobject("dm.dmsoft")  
  
dm.SetPath dm.GetBasePath()  
hwnd = dm.FindWindowSuper("sub",0,1,"subWin",2,1)  
hwnd2 = dm.GetWindow(hwnd,0)  
  
// 两个对象分别绑定对应的窗口  
dm\_ret = dm.BindWindowEx(hwnd,"dx.graphic.opengl","windows","windows","",0)  
dm\_ret2 =
dm2.BindWindowEx(hwnd2,"normal","dx.mouse.position.lock.api","dx.keypad.input.lock.api","",0)  
TracePrint dm\_ret  
TracePrint dm\_ret2  
  
// dm用于图色 dm2用于键鼠. 结合起来. 让dm同时处理图色和键鼠  
TracePrint dm.SetInputDm(dm2.GetId(),0,0)  
  
// 正常进行处理.比如找图 找字等等.  
dm\_ret =
dm.FindPic(0,0,2000,2000,"test.bmp","000000",0.9,0,x,y)  
TracePrint cstr(x)  
if x > 0 then  
   dm.MoveTo x,y  
   delay 100  
   dm.LeftClick  
end if  
  
...  
  
// 解绑  
dm.UnBindWindow  
dm2.UnBindWindow

注: 此接口用于特殊用途.   
比如雷电模拟器. 最里层的窗口是一个64位窗口. 绑定这个窗口的图色可以用来图色后台.
但是这个窗口无法进行键鼠后台.  
能够键鼠窗口后台的是这个窗口的上一层32位窗口.但这个32位窗口在某些情况下图色会出问题.  
所以比较好的解决办法是创建2个对象. 一个绑定64位的窗口，用来进行图色使用. 另一个绑定32位的窗口,用来进行键鼠操作.

但是如果对于写好的代码来说,更改起来很麻烦. 因为大部分情况下一个对象就够用了.为了让代码不用大幅度更改,就加了这样一个接口.  
让进行图色绑定的那个对象和进行键鼠操作的那个对象结合起来. 这样只用操作一个图色绑定的对象就行了.  
  
这里要注意的是,如果2个对象对应的窗口不是一个进程,那么绑定参数上没什么要求. 如果是一个进程,那么必须保证只有一个对象能够使用注入的参数.否则会引发冲突导致崩溃.  
还有rx和ry的具体含义. 解释如下:  
一般来说,我们调用MoveTo或者MoveToEx时,传递进来的x和y坐标都是来自于图色窗口,但是键鼠操作的那个窗口是另一个窗口. 如果这2个窗口左上角是重合的,那么无所谓  
rx和ry就是0. 比如我们这里的雷电模拟器等窗口.  
但是如果不重合,那么我们传递给MoveTo或者MoveToEx的x和y就和键鼠操作的窗口的x和y不对应. 所以就必须从图色的x,y减去两个窗口的左上角偏移,这样才能对应键鼠操作的窗口.

一般来说,rx和ry都是0. 可能有极少数有这种不为0的特例(我是暂时没发现). 这里的rx和ry必须是键鼠操作的窗口左上角减去图色窗口的左上角,不能是反的.

另外在解绑时,会自动重置. 即图色窗口的对象自动和键鼠窗口的对象脱离.   
需要注意的是,因为两个对象进行了结合,那么就要确保两个对象的生命周期必须是一致的. 尤其千万不能在图色窗口操作时,键鼠对象被释放了. 那么会导致程序的崩溃.

这个接口影响的输入接口如下列表(即图色对象调用了SetDmInput后,以下这些接口统统都是对键鼠对象的调用)

GetCursorPos  
GetCursorShape  
GetCursorShapeEx  
GetCursorSpot  
KeyDown  
KeyDownChar  
KeyPress  
KeyPressChar  
KeyPressStr  
KeyUp  
KeyUpChar  
LeftClick  
LeftDoubleClick  
LeftDown  
LeftUp  
MiddleClick  
MiddleDown  
MiddleUp  
MoveR  
MoveTo  
MoveToEx  
RightClick  
RightDown  
RightUp  
SetKeypadDelay  
SetMouseDelay  
SetSimMode  
WheelDown  
WheelUp  
  
EnableFakeActive  
EnableKeypadMsg  
EnableKeypadPatch  
EnableKeypadSync  
EnableMouseMsg  
EnableMouseSync  
EnableRealKeypad  
EnableRealMouse  
EnableSpeedDx  
LockInput