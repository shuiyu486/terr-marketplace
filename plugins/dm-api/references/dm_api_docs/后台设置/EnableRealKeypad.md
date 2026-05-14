函数简介:

键盘动作模拟真实操作,点击延时随机.

函数原型:  
  
long EnableRealKeypad(enable)

参数定义:

enable
整形数: 0 关闭模拟  
              
1 开启模拟

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm.EnableRealKeypad 1

dm.KeyPressChar "E"

注: 此接口对KeyPress KeyPressChar KeyPressStr起作用。具体表现是键盘按下和弹起的间隔会在  
当前设定延时的基础上,上下随机浮动50%. 假如
设定的键盘延时是100,那么这个延时可能就是50-150之间的一个值.

设定延时的函数是 SetKeypadDelay