函数简介:

获取鼠标热点位置.(参考工具中抓取鼠标后，那个闪动的点就是热点坐标,不是鼠标坐标)

当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，

获取到的是后台鼠标热点位置，否则是前台鼠标热点位置.  [关于如何识别后台鼠标特征.](../常见问题/如何可以后台识别鼠标特征码.htm)

函数原型:  
  
string GetCursorSpot()

参数定义:

返回值:

字符串:  
成功时，返回形如"x,y"的字符串    
失败时，返回空的串.

示例:

hot\_pos = dm.GetCursorSpot()  
if len(hot\_pos) > 0 Then  
    hot\_pos
= split(hot\_pos,",")  
    x = int(hot\_pos(0))  
    y = int(hot\_pos(1))  
end if