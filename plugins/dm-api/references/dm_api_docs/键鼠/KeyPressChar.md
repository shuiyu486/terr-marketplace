函数简介:

按下指定的虚拟键码

函数原型:  
  
long KeyPressChar(key\_str)

参数定义:  
  
key\_str字符串**:** 字符串描述的键码. 大小写无所谓**. [点这里查看具体对应关系](键码对应表.htm).**

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.KeyPressChar "enter"  
dm.KeyPressChar "1"  
dm.KeyPressChar "F1"  
dm.KeyPressChar "a"  
dm.KeyPressChar "B"