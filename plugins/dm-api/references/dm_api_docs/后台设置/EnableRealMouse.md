函数简介:

鼠标动作模拟真实操作,带移动轨迹,以及点击延时随机.

函数原型:  
  
long EnableRealMouse(enable,mousedelay,mousestep)

参数定义:

enable
整形数: 0 关闭模拟  
              
1 开启模拟(直线模拟)  
              
2 开启模拟(随机曲线,更接近真实)  
              
3 开启模拟(小弧度曲线,弧度随机)  
              
4 开启模拟(大弧度曲线,弧度随机)

mousedelay
整形数: 单位是毫秒. 表示在模拟鼠标移动轨迹时,每移动一次的时间间隔.这个值越大,鼠标移动越慢. 必须大于0,否则会失败.

Mousestep
整形数: 表示在模拟鼠标移动轨迹时,每移动一次的距离. 这个值越大，鼠标移动越快速.

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm.EnableRealMouse 1,20,30

dm.MoveTo 100,100  
dm.MoveTo 500,500

注: 此接口同样对LeftClick RightClick MiddleClick LeftDoubleClick起作用。具体表现是鼠标按下和弹起的间隔会在  
当前设定延时的基础上,上下随机浮动50%. 假如
设定的鼠标延时是100,那么这个延时可能就是50-150之间的一个值.

设定延时的函数是
SetMouseDelay