出现这种问题，99%的原因是由于插件版本没有注册到系统导致,解决办法如下  
  
1. 删除Plugin目录的dm.dll和dm\_jdyou.dll (简单游的话直接删除bin目录)

2. 插件的释放路径不要释放到Plugin目录，改为c盘的某个目录
，并且用RegDll来注册，如下  
PutAttachment "c:\test\_game"
,"\*.\*"  
PutAttachment ".\Plugin"
,"RegDll.dll"  
Call Plugin.RegDll.Reg("c:\test\_game\dm.dll")

3. 重新启动脚本即可

4. 如果这样还不行，尝试手动注册，手动在运行下，输入regsvr32 c:\test\_game\dm.dll,

如果这样还提示出错，那就是系统问题，重装干净安全的系统.

最好不要用ghost系统，很多ghost系统都是修改过系统文件的，很危险!

从2.1118B版本之后，大漠插件将禁止释放到Plugin目录，以避免一系列升级产生的BUG！  
同时，也禁止用Plugin方式来调用插件，那个方式也是非常不安全的.  
请大家严格按照vbs的语法来使用插件.