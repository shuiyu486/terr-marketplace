函数简介:

利用真实的输入法，对指定的窗口输入文字.

函数原型:  
  
long SendStringIme2(hwnd,str,mode)

参数定义:  
  
hwnd整形数: 窗口句柄  
str 字符串: 发送的文本数据  
mode整形数: 取值意义如下:  
           
0 : 向hwnd的窗口输入文字(前提是必须先用模式200安装了输入法)  
           
1 : 同模式0,如果由于保护无效，可以尝试此模式.(前提是必须先用模式200安装了输入法)  
           
2 : 同模式0,如果由于保护无效，可以尝试此模式. (前提是必须先用模式200安装了输入法)  
           
200 : 向系统中安装输入法,多次调用没问题. 全局只用安装一次.  
           
300 : 卸载系统中的输入法. 全局只用卸载一次. 多次调用没关系.

返回值:

整形数:  
0: 失败  
1: 成功

示例:

If
dm.SendStringIme2(hwnd,"",200) = 1 then  
     
dm.SendStringIme2 hwnd,"我是来测试的",0  
     
dm.SendStringIme2 hwnd,"abc",0  
     
dm.SendStringIme2 hwnd,"123",0  
     
dm.SendStringIme2 hwnd,"",300  
end if 

注: 如果要同时对此窗口进行绑定，并且绑定的模式是1 3 5 7 101 103，那么您必须要在绑定之前,先执行加载输入法的操作. 否则会造成绑定失败!.  
卸载时，没有限制.  
还有，在后台输入时，如果目标窗口有判断是否在激活状态才接受输入文字,那么可以配合绑定窗口中的假激活属性来保证文字正常输入. 诸如此类. 基本上用这个没有输入不了的文字.  
比如  
BindWindow
hwnd,"normal","normal","normal","dx.public.active.api|dx.public.active.message",0  
dm.SendStringIme2 hwnd,"哈哈",0