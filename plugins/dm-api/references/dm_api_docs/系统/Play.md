函数简介:

播放指定的MP3或者wav文件.

函数原型:  
  
long Play(media\_file)

参数定义:

media\_file 字符串: 指定的音乐文件，可以采用文件名或者绝对路径的形式.

返回值:

整形数:  
0 : 失败  
非0表示当前播放的ID。可以用Stop来控制播放结束.

示例:

// test.mp3放于d:\test目录下  
dm.SetPath "d:\test"  
id = dm.Play("test.mp3")

// 绝对路径  
id = dm.Play("d:\test\test.mp3")  
Delay 1000  
dm.Stop id