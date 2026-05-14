函数简介:

释放插件用的驱动. 可以自己拿去签名. 防止有人对我的签名进行检测. 强烈推荐使用驱动的用户使用. 仅释放64位系统的驱动.

函数原型:  
  
long DmGuardExtract(type,path)

参数定义:

type 字符串: 需要释放的驱动类型. 这里写"common"即可.

path 字符串: 释放出的驱动文件全路径. 比如"c:\test.sys".

返回值:  
  
整形数:  
0 : 不支持的type  
1 : 成功  
-2: 释放失败

示例:  
  
dm.DmGuardExtract "common","c:\test.sys"

注 : 释放出的文件进行签名后,可以再用DmGuardLoadCustom来进行加载.