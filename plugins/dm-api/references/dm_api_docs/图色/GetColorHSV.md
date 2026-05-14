函数简介:

获取(x,y)的HSV颜色,颜色返回格式"H.S.V"

函数原型:  
  
string GetColorHSV(x,y)

参数定义:  
  
x 整形数:X坐标  
y 整形数:Y坐标

返回值:

字符串:  
颜色字符串

示例:

color = dm.GetColorHSV(30,30)  
If color = "100.20.20" Then  
      MessageBox
"ok"  
End If