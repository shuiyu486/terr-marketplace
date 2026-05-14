函数简介:

加载用DmGuardExtract释放出的驱动. 建议自己签名后,然后找个自己喜欢的路径加载. 仅支持64位系统的驱动加载.

加载成功后,就可以正常调用DmGuard了.

函数原型:  
  
long DmGuardLoadCustom(type,path)

参数定义:

type 字符串: 需要释放的驱动类型. 这里写"common"即可.

path 字符串:驱动文件全路径. 比如"c:\test.sys".

返回值:  
  
整形数:  
返回值请参考DmGuard的返回值. 一样的含义.

示例:  
  
dm.DmGuardLoadCustom "common","c:\test.sys"

注 : 这个路径只是演示. 实际上最好不要放在这么随意的位置. 一般驱动文件都在c:\windows\system32目录下.