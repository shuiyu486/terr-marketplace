函数简介:

停止指定的音乐.

函数原型:  
  
long Stop(id)

参数定义:

id 整形数: Play返回的播放id.

返回值:

整形数:  
0 : 失败  
1 : 成功.

示例:

// test.mp3放于d:\test目录下  
dm.SetPath "d:\test"  
id = dm.Play("test.mp3")

// 绝对路径  
id = dm.Play("d:\test\test.mp3")  
Delay 1000  
dm.Stop id