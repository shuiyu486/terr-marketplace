函数简介:

检测系统中是否安装了指定输入法

函数原型:  
  
long FindInputMethod(input\_method)

参数定义:  
  
input\_method 字符串: 输入法名字。
具体输入法名字对应表查看注册表中以下位置:

HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard
Layouts

下面的每一项下的Layout Text的值就是输入法名字

比如 "中文 - QQ拼音输入法"

以此类推.

返回值:

整形数:  
0 : 未安装

1 : 安装了

示例:

dm\_ret = dm.FindInputMethod("中文 - QQ拼音输入法")  
if dm\_ret = 1 then  
    msgbox "QQ输入法安装啦"  
end if