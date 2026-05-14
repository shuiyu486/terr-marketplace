函数简介:

设置当前系统的硬件加速级别.

函数原型:  
  
long SetDisplayAcceler(level)

参数定义:

level整形数: 取值范围为0-5.  0表示关闭硬件加速。5表示完全打开硬件加速.

返回值:  
  
整形数:  
0 : 失败.

1 : 成功.

示例:

// 关闭硬件加速  
TracePrint SetDisplayAcceler(0)

注: 此函数只在XP 2003系统有效.