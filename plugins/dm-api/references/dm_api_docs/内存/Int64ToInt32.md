函数简介:

强制转换64位整数为32位. (这个函数是给按键精灵设计的,由于按键精灵不支持64位自动化变量,某些返回64位的整数的接口会出错)

函数原型:  
  
long Int64ToInt32(value)

参数定义:  
  
value 长整形数: 需要转换的64位整数

返回值:

整形数:  
返回的32位整数

示例:

base\_addr = dm.Int64ToInt32(dm.GetMoudleBaseAddr(hwnd,"ntdll.dll"))