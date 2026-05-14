# DmGuardParams

**分类:** 防护盾

**签名:** `string DmGuardParams(cmd,subcmd,param)`

**描述:** DmGuard的加强接口,用于获取一些额外信息. 具体看下面参数介绍

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| cmd | str | 盾类型. 这里取值为"gr"或者"th"(以后可能会有扩充). 这里要注意的是,如果要获取指定的盾类型信息,必须先成功用DmGuard开启此盾.比如这里的"gr"必须dm.DmGuard |
| subcmd | str | 针对具体的盾类型，需要获取的具体信息. 如果cmd为"gr"时,那么subcmd取值如下定义: "enum" : 枚举指定进程的所有句柄. "get"  : 获取指定进程的指定句柄信息.(类型,名字,权限值) "set"  : 设置指定进程的指定句柄的权限值. "close": 关闭指定进程的指定句柄. 如果cmd为"th"时,那么subcmd取值如下定义: "enum" :    枚举指定进程的所有线程. "get"  :    获取指定线程的详细信息.(句柄值,优先级,ETHREAD,TEB,win32StartAddresss,线程地址所在的模块名,交换次数,线程状态,挂起次数) "resume"  : 恢复指定的线程.不可操作本线程. 当suspend_count大于0时,每调用一次resume,都会让suspend_count减1,直到0为止才会真正的恢复线程. "suspend":  挂起指定线程.不可操作本线程. "terminate":结束指定线程.不可操作本线程. |
| param | str | 参数信息,这里具体的含义取决于cmd和subcmd. 如果cmd为"gr"时,subcmd取值为如下时，具体的参数含义: "enum" : param为"pid", pid为进程pid,10进制形式. "get"  : param为"pid handle",pid为进程pid,10进制形式,handle为句柄值,10进制形式. "set"  : param为"pid handle access",pid为进程pid,10进制形式,handle为句柄值,10进制形式,access为权限值,10进制形式. "close": param为"pid handle", pid为进程pid,10进制形式,handle为句柄值,10进制形式. 如果cmd为"th"时,subcmd取值为如下时，具体的参数含义: "enum" :     param为"pid", pid为进程pid,10进制形式. "get"  :     param为"tid", tid为线程tid,10进制形式. "resume"  :  param为"tid", tid为线程tid,10进制形式. "suspend"  : param为"tid", tid为线程tid,10进制形式. "terminate": param为"tid", tid为线程tid,10进制形式. |

## 返回值

- 字符串: 根据不同的cmd和subcmd,返回值不同. 如果cmd为"gr"时,subcmd取值为如下时，具体的返回值: "enum" : "handle1|handle2|.....|handlen",每个handle都是10进制长整数. 如果失败返回空字符串 "get"  : "type|name|access". type表示句柄的类型，比如"Event","File"等之类的. name表示句柄的名字,有些句柄的名字可能是空的. access10进制整数,表示此句柄的权限值. 如果失败返回空字符串 "set"  : 成功返回"ok",否则为空字符串. "close": 成功返回"ok",否则为空字符串. 如果cmd为"th"时,subcmd取值为如下时，具体的返回值: "enum" : "tid1|tid2|.....|tidn",每个tid都是10进制整数. 如果失败返回空字符串 "get"  : "tid|prority|ethread|teb|win32StartAddress|module\_name|switch\_count|state|suspend\_count".如果失败返回空字符串. tid : 线程tid,10进制整数 prority : 线程优先级, 10进制整数 ethread : 线程内核对象ETHREAD指针. 64位16进制整数. teb : 线程内核对象TEB指针. 64位16进制整数 win32StartAddress : 线程起始地址. 64位16进制整数 module\_name : 线程起始地址所在的模块名. switch\_count : 线程切换次数.
- 10进制整数 state : 线程状态. 10进制整数. 0 : 初始化 1 : 准备 2 : 运行 3 : 待机 4 : 结束 5 : 等待 6 : 转换. 这个地方其实只需要关心是不是4就行了. 如果是4表示线程结束了. 其它的状态都可以认为是运行状态. 不用太关心. suspend\_count : 线程挂起次数.
- 10进制整数. 线程挂起次数,当此值大于0时,表示线程处于挂起状态. 等于0表示处于运行状态. "resume"  : 成功返回"ok",否则为空字符串. "suspend": 成功返回"ok",否则为空字符串. "terminate": 成功返回"ok",否则为空字符串.

## 示例

```vbs
// 枚举进程的所有句柄,并获取此句柄的信息,并打印出来
dm_ret = dm.DmGuard(1,"gr")
dm_ret = dm.DmGuardParams("gr","enum","1024")

If len(dm_ret) > 0 Then
ss
= split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
dm_ret = dm.DmGuardParams("gr","get","1024
" & ss(index))
TracePrint dm_ret
index =
index +1
Loop
End If

// 关闭指定进程的句柄
dm_ret = dm.DmGuard(1,"gr")
dm_ret = dm.DmGuardParams("gr","close","1024
240")
TracePrint dm_ret

// 修改指定进程的句柄的权限
dm_ret = dm.DmGuard(1,"gr")
dm_ret = dm.DmGuardParams("gr","set","1024
240 12345")
TracePrint dm_ret

// 枚举进程的所有线程,并把线程的信息都打印出来
dm_ret = dm.DmGuard(1,"th")
dm_ret = dm.DmGuardParams("th","enum","1024")

If len(dm_ret) > 0 Then
ss
= split(dm_ret,"|")
index = 0
count = UBound(ss) + 1
Do While index < count
dm_ret = dm.DmGuardParams("th","get",ss(index))
TracePrint dm_ret
index =
index +1
Loop
End If

// 结束指定线程. 注意后面的338是线程tid. 不是进程pid
dm_ret = dm.DmGuardParams("th","terminate","338")
// 挂起指定线程
dm_ret = dm.DmGuardParams("th","suspend","338")
// 恢复指定线程
dm_ret = dm.DmGuardParams("th","resume","338")
```

## 注意

- gr盾对应的这些subcmd,其实最主要的目的是"set", 设置句柄权限.
- 比如场景1:
- 我们需要打开进程，或者打开线程，文件等等，如果在打开进程的权限里写了最高权限，那么由于一些保护措施，往往会失败. 但是如果你降低一些权限，比如用最低权限，反而会成功. 所以我们可以先用低权限打开对应的句柄,然后用"set"来提权，这样就相当于用间接的方式用最高权限打开了句柄.
- 再比如场景2:
- 某些时候，有坏人打开我们自己的进程来做一些非法的事情,这时候我们可以通过扫描("enum"功能),来检查是否有关我们进程的句柄,如果有的话，我们可以考虑直接关闭句柄("close"),或者给他降低权限("set").
- 其它场景，请自行脑补. 可能又有人会问,我怎么知道设定的权限值到底是多少呢？ 这个很简单。 每种句柄都对应不同的权限，我们可以自己创建一个最高权限的句柄，来获取("get")这个句柄的信息，就知道最高权限对应的权限到底是多少. 同样最低权限也一样。
- 这里一定要注意,不同类型的句柄,权限定义是不同的. 比如"Event"和"File"就是完全不同的权限值.
- 这里对进程句柄举个例子. 比如我们想获取最高权限的进程句柄权限值,那么操作如下
- // 我们打开进程id为1024的句柄, 1024只是一个例子，必须换成真实存在的pid
- handle = dm.OpenProcess(1024)
- dm\_ret = dm.DmGuard(1,"gr")
- my\_pid = GetCurrentProcessId()
- // 这个GetCurrentProcessId是调用系统API，获取当前进程ID，因为打开的句柄在本进程里
- info = dm.DmGuardParams("gr","get",cstr(my\_pid)& " " & cstr(handle))
- ss = split(info,"|")
- access = clng(ss(2))
- // 那么这里的access就是最高权限的值了.
- 一般来说,每种句柄权限在不同系统里的定义都是相同的. 所以你可以在一个系统里获取到后，在其它系统里也是通用的.
- ps : 上次有人问我，如何把一个别人正在读写的文件给强行打开读写，其实也是一个权限的事,增加一个SHARE\_READ和SHARE\_WRITE就OK了. 具体方法和上面这个进程句柄大同小异.
