函数简介:

锁定指定窗口的图色数据(不刷新).

函数原型:  
  
long LockDisplay(lock)

参数定义:

lock 整形数: 0关闭锁定  
            
1 开启锁定

返回值:

整形数:  
0: 失败  
1: 成功

示例:

dm\_ret = dm.BindWindow(hwnd,"dx","dx2","dx",0)  
dm.LockDisplay 1  
// 这里做需要锁定做的事情  
dm.LockDisplay 0

注意: 此接口只对图色为dx.graphic.3d  dx.graphic.3d.8
dx.graphic.2d  dx.graphic.2d.2 dx.graphic.3d.10plus有效.