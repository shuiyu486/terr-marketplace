函数简介:

查找指定区域内的所有颜色块,颜色格式"RRGGBB-DRDGDB",注意,和按键的颜色格式相反

函数原型:  
  
string FindColorBlockEx(x1,
y1, x2, y2, color, sim, count, width, height)

参数定义:  
  
x1 整形数:区域的左上X坐标  
y1 整形数:区域的左上Y坐标  
x2 整形数:区域的右下X坐标  
y2 整形数:区域的右下Y坐标  
color 字符串:颜色 格式为"RRGGBB-DRDGDB" 比如"aabbcc-000000|123456-202020".也可以支持反色模式. 前面加@即可. 比如"@123456-000000|aabbcc-202020". 具体可以看下放注释.注意，这里只支持RGB颜色.  
sim 双精度浮点数:相似度,取值范围0.1-1.0  
count整形数:在宽度为width,高度为height的颜色块中，符合color颜色的最小数量.(注意,这个颜色数量可以在综合工具的二值化区域中看到)  
width 整形数:颜色块的宽度  
height 整形数:颜色块的高度

返回值:

字符串:  
返回所有颜色块信息的坐标值,然后通过GetResultCount等接口来解析 (由于内存限制,返回的颜色数量最多为1800个左右)

示例:

s = dm.FindColorBlockEx(0,0,2000,2000,"123456-000000|abcdef-202020",1.0,350,100,200)  
count = dm.GetResultCount(s)  
index = 0  
Do While index < count  
    dm\_ret
= dm.GetResultPos(s,index,intX,intY)  
    MessageBox
intX&","&intY   
    index = index + 1   
Loop

注: 反色模式是指匹配任意一个指定颜色之外的颜色. 比如"@123456|333333". 在匹配时,会匹配除了123456或者333333之外的颜色.