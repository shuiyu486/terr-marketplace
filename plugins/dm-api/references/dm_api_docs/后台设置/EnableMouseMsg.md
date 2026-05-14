函数简介:

是否在使用dx鼠标时开启windows消息.默认开启.

函数原型:  
  
long EnableMouseMsg(enable)

参数定义:

enable
整形数: 0 禁止  
              
1开启

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)  
dm.EnableMouseMsg 0

注: 此接口必须在绑定之后才能调用。特殊时候使用.