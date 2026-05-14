函数简介:

鼠标消息采用同步发送模式.默认异步.

函数原型:  
  
long EnableMouseSync(enable,time\_out)

参数定义:

enable
整形数: 0 禁止同步  
              
1开启同步

time\_out
整形数: 单位是毫秒,表示同步等待的最大时间.

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)  
dm.EnableMouseSync 1,200

注: 此接口必须在绑定之后才能调用。

有些时候，如果是异步发送，如果发送动作太快,中间没有延时,有可能下个动作会影响前面的.

而用同步就没有这个担心.