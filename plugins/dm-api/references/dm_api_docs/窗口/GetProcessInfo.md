函数简介:

根据指定的pid获取进程详细信息,(进程名,进程全路径,CPU占用率(百分比),内存占用量(字节))

函数原型:  
  
string GetProcessInfo(pid)

参数定义:

pid 整形数: 进程pid

返回值:  
  
字符串:  
格式"进程名|进程路径|cpu|内存"

示例:

infos = dm.GetProcessInfo(1348)   
infos = split(infos,"|")  
TracePrint "进程名:"&infos(0)  
TracePrint "进程路径:"&infos(1)  
TracePrint "进程CPU占用率(百分比):"&infos(2)  
TracePrint "进程内存占用量(字节):"&infos(3)

注: 有些时候有保护的时候，此函数返回内容会错误，那么此时可以尝试用memory保护盾来试试看.  
另外此接口调用会延迟1秒.