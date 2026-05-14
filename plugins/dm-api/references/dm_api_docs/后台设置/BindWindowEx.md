# BindWindowEx

**分类:** 后台设置

**签名:** `long BindWindowEx(hwnd,display,mouse,keypad,public,mode)`

**描述:** 绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式 高级用户使用.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄 |
| display | str | 屏幕颜色获取方式 取值有以下几种 "normal" : 正常模式,平常我们用的前台截屏模式 "gdi" : gdi模式,用于窗口采用GDI方式刷新时. 此模式占用CPU较大. 参考[SetAero](SetAero.htm). win10以上系统使用此模式，如果截图失败，尝试把目标程序重新开启再试试。 "gdi2" : gdi2模式,此模式兼容性较强,但是速度比gdi模式要慢许多,如果gdi模式发现后台不刷新时,可以考虑用gdi2模式. "dx2" : dx2模式,用于窗口采用dx模式刷新,如果dx方式会出现窗口进程崩溃的状况,可以考虑采用这种.采用这种方式要保证窗口有一部分在屏幕外.win7 win8或者vista不需要移动也可后台. 此模式占用CPU较大. 参考[SetAero](SetAero.htm). win10以上系统使用此模式，如果截图失败，尝试把目标程序重新开启再试试。 "dx3" : dx3模式,同dx2模式,但是如果发现有些窗口后台不刷新时,可以考虑用dx3模式,此模式比dx2模式慢许多. 此模式占用CPU较大. 参考[SetAero](SetAero.htm). win10以上系统使用此模式，如果截图失败，尝试把目标程序重新开启再试试。 dx模式,用于窗口采用dx模式刷新,取值可以是以下任意组合，组合采用"|"符号进行连接. 支持BindWindow中的缩写模式. 比如dx代表" dx.graphic.2d| dx.graphic.3d" |
| mouse | str | 鼠标仿真模式 取值有以下几种 "normal" : 正常模式,平常我们用的前台鼠标模式 "windows": Windows模式,采取模拟windows消息方式 同按键的后台插件. "windows3": Windows3模式，采取模拟windows消息方式,可以支持有多个子窗口的窗口后台 dx模式,取值可以是以下任意组合. 组合采用"|"符号进行连接. 支持BindWindow中的缩写模式,比如windows2代表"dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.state.message" |
| keypad | str | 键盘仿真模式 取值有以下几种 "normal" : 正常模式,平常我们用的前台键盘模式 "windows": Windows模式,采取模拟windows消息方式 同按键的后台插件. dx模式,取值可以是以下任意组合. 组合采用"|"符号进行连接. 支持BindWindow中的缩写模式.比如dx代表" dx.public.active.api|dx.public.active.message| dx.keypad.state.api|dx.keypad.api|dx.keypad.input.lock.api" |
| public | str | 公共属性 dx模式共有 取值可以是以下任意组合. 组合采用"|"符号进行连接 这个值可以为空 |
| mode | int | 模式。 取值有以下几种 |

## 返回值

- 0: 失败
- 1: 成功 如果返回0，可以调用[GetLastError](../基本设置/GetLastError.htm)来查看具体失败错误码,帮助分析问题.

## 示例

```vbs
比如
dm_ret = dm.BindWindowEx(hwnd,"normal","dx.mouse.position.lock.api|dx.mouse.position.lock.message","windows","dx.public.active.api",0)

dm_ret = dm.BindWindowEx(hwnd,"dx2","windows","normal","dx.public.active.api",0)

dm_ret = dm.BindWindowEx(hwnd,"dx.graphic.2d","dx.mouse.position.lock.api|dx.mouse.position.lock.message","dx.keypad.state.api|dx.keypad.api","",0)

dm_ret = dm.BindWindowEx(hwnd,"dx2","windows","windows","",0)

dm_ret = dm.BindWindowEx(hwnd,"dx2","windows","windows","dx.public.disable.window.size|dx.public.disable.window.minmax",0)

dm_ret = dm.BindWindowEx(hwnd,"dx2","windows3","windows","dx.mouse.position.lock.api",0)

等等.
```

## 注意

- 绑定之后,所有的坐标都相对于窗口的客户区坐标(不包含窗口边框)
- 另外,绑定窗口后,必须加以下代码,以保证所有资源正常释放
- 这个函数的意思是在脚本结束时,会调用这个函数。需要注意的是，目前的按键版本对于这个函数的执行不是线程级别的，也就是说，这个函数只会在主线程执行，子线程绑定的大漠对象，不保证完全释放。高级语言中则需要自己控制在适当的时候解除绑定.
- Sub OnScriptExit()
- dm\_ret =
- dm.UnBindWindow()
- End Sub
- 另外 绑定dx会比较耗时间,请不要频繁调用此函数.
- 还有一点特别要注意的是,有些窗口绑定之后必须加一定的延时,否则后台也无效.一般1秒到2秒的延时就足够.
- 发现绑定失败的几种可能(一般是需要管理员权限的模式才有可能会失败)
- 系统登录的帐号必须有Administrators权限
- 一些防火墙会防止插件注入窗口所在进程，比如360防火墙等，必须把dm.dll设置为信任.
- 还有一个比较弱智的可能性，那就是插件没有注册到系统中，这时CreateObject压根就是失败的. 检测对象是否创建成功很简单，如下代码
- set dm = createobject("dm.dmsoft")
- ver = dm.Ver()
- If len(ver) = 0 Then
- MessageBox "创建对象失败,检查系统是否禁用了vbs脚本权限"
- EndScript
- End If
- 在沙盘中开的窗口，绑定一些需要管理员权限的模式，会失败。
- 解决方法是要配置沙盘参数，参考如何配置沙盘参数.
- 窗口所在进程有保护，这个我也无能为力.
