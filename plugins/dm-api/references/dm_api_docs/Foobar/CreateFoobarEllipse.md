函数简介:

创建一个椭圆窗口

函数原型:  
  
long CreateFoobarEllipse(hwnd,x,y,w,h)

参数定义:  
  
hwnd整形数: 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口  
  
x整形数: 左上角X坐标(相对于hwnd客户区坐标)

y整形数: 左上角Y坐标(相对于hwnd客户区坐标)

w整形数: 矩形区域的宽度

h整形数: 矩形区域的高度

返回值:  
  
整形数 : 创建成功的窗口句柄

示例:

foobar = dm.CreateFoobarEllipse(hwnd,10,10,200,200)

注: foobar不能在本进程窗口内创建.