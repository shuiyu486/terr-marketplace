函数简介:

对指定的数据地址和长度，组合成新的参数.
FindPicMem FindPicMemE 以及FindPicMemEx专用

函数原型:  
  
string AppendPicAddr(pic\_info,addr,size)

参数定义:

pic\_info 字符串: 老的地址描述串

addr 整形数: 数据地址

size 整形数: 数据长度

返回值:  
  
字符串:  
新的地址描述串

示例:

pic\_info = ""  
pic\_info = dm.AppendPicAddr(pic\_info,12034,643)  
pic\_info = dm.AppendPicAddr(pic\_info,328435,8935)  
pic\_info = dm.AppendPicAddr(pic\_info,809234,789)