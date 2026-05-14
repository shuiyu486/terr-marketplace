函数简介:

获取(x,y)的颜色,颜色返回格式"BBGGRR"

函数原型:  
  
string GetColorBGR(x,y)

参数定义:  
  
x 整形数:X坐标  
y 整形数:Y坐标

返回值:

字符串:  
颜色字符串(注意这里都是小写字符，和工具相匹配)

示例:

color = dm.GetColorBGR(30,30)  
If color = "0000ff" Then  
      MessageBox
"是红色"  
End If