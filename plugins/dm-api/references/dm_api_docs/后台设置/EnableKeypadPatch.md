函数简介:

键盘消息发送补丁. 默认是关闭.

函数原型:  
  
long EnableKeypadPatch(enable)

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
dm.EnableKeypadPatch 1

注: 此接口必须在绑定之后才能调用。