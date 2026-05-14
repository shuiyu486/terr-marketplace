函数简介:

加密指定的文件.

函数原型:  
  
long EncodeFile(file,pwd)

参数定义:

file 字符串: 文件名.

pwd 字符串: 密码.

返回值:  
  
整形数:  
0 : 失败  
1 : 成功

示例:  
  
// 绝对路径  
dm.EncodeFile "c:\test\_game\cfg.ini","1234"  
  
// 相对路径  
dm.SetPath "c:\test\_game"  
dm.EncodeFile "1.bmp","1234"

如果此文件已经加密，调用此函数不会有任何效果.  
插件所有的字库 图片 ini都是用此接口来加密.