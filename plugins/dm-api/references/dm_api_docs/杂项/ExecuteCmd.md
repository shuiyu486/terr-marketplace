# ExecuteCmd

**分类:** 杂项

**签名:** `string ExecuteCmd(cmd,current_dir,time_out)`

**描述:** 执行指定的CMD指令,并返回cmd的输出结果.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| cmd | str | 需要执行的CMD指令. 比如"dir" |
| current_dir | str | 执行此cmd命令时,所在目录. 如果为空，表示使用当前目录. 比如""或者"c:" |
| time_out | int | 超时设置,单位是毫秒. 0表示一直等待. 大于0表示等待指定的时间后强制结束,防止卡死. |

## 返回值

- 字符串: cmd指令的执行结果.  返回空字符串表示执行失败.

## 示例

```vbs
TracePrint dm.ExecuteCmd("dir","",0)
TracePrint dm.ExecuteCmd("dir","c:",2000)
TracePrint dm.ExecuteCmd("dir","c:\windows",3000)

介于很多人不会用命令行操作CMD,这里写一份常用的adb命令来给大家参考.

首先,adb.exe是一个操作android系统的应用程序，一般都在你安装的模拟器的对应的目录下.

比如雷电模拟器,我们假如安装再d:\dnplayer2,那么adb.exe一般就位于这个目录.
其它模拟器同理.

知道adb.exe的路径，那么我们就开始调用adb来实现一些常用的功能. 以下所有的例子，都假定adb.exe位于d:\dnplayer2

1. 查看adb的版本信息. 这个可以用于测试adb.exe是否是你想要的版本,如下:

**adb_version
= dm.ExecuteCmd("adb.exe
version","d:\dnplayer2",0)**

**TracePrint
adb_version**

比如我的机器的返回值是以下内容

Android Debug Bridge
version 1.0.31

2. 接下来我们开始对模拟器里的东东做一些操作.比如安装APK，拷贝文件之类的。 我们首先要先列出当前系统的所有device(可以是模拟器，也可以是用USB连接的手机),例子如下:

**adb_devices
= dm.ExecuteCmd("adb.exe devices","d:\dnplayer2",0)**

**TracePrint
adb_devices**

比如我的机器的返回值如下:(我打开了2个模拟器)

List of devices attached

127.0.0.1:5555    device

127.0.0.1:5557    device

这里要说明一下,前面这个IP地址和端口号，就标识了一个device,我们后面要操作这些devcie，必须依赖于这个标识.

有的时候，这个标识不一定是ip地址和端口号，也可能是序列号之类的东西. 但意思都一样.

3. 接下来我们来对127.0.0.1:5555这个device来查看下安装的应用,例子如下:(这里我们要用到adb
shell命令,顾名思义，这个shell的意思就是去device上去执行命令,这里的语法都和linux的语法一样)

**adb_device_1_apps
= dm.ExecuteCmd("adb.exe -s 127.0.0.1:5555 shell pm list
packages","d:\dnplayer2",0)**

**TracePrint
adb_device_1_apps**

这里输出的内容比较多，我就不列举了

简单的说一下，这里的**-s****设备标识** 的意思就是对这台device来执行命令.  设备标识在之前adb
devices中有列出来.

那么我们要执行其它的操作，也是如此,比如**"adb.exe -s 设备标识  命令"**

比如安装apk

**dm.ExecuteCmd("adb.exe
-s 127.0.0.1:5555 install -r d:\xxx.apk","d:\dnplayer2",0)**

比如卸载某apk

**dm.ExecuteCmd("adb.exe
-s 127.0.0.1:5555 uninstall
com.qihoo360.mobilesafe","d:\dnplayer2",0)**

好到此为止，如何操作adb去控制模拟器，就说到这里。

这里贴一份常用详细的adb中文说明给大家参考

https://blog.csdn.net/u010375364/article/details/52344120
```
