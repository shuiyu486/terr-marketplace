函数简介:

获取(x,y)的颜色,颜色返回格式"RRGGBB",注意,和按键的颜色格式相反

函数原型:  
  
string GetColor(x,y)

参数定义:  
  
x 整形数:X坐标  
y 整形数:Y坐标

返回值:

字符串:  
颜色字符串(注意这里都是小写字符，和工具相匹配)

示例:

color = dm.GetColor(30,30)  
If color = "ffffff" Then  
     MessageBox
"是白色"  
End If