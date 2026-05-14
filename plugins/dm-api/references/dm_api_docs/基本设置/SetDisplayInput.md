函数简介:

设定图色的获取方式，默认是显示器或者后台窗口(具体参考BindWindow)

函数原型:  
  
long SetDisplayInput(mode)

参数定义:  
  
mode 字符串: 图色输入模式
取值有以下几种

1.    
"screen"
这个是默认的模式，表示使用显示器或者后台窗口

2.    
"pic:file" 指定输入模式为指定的图片,如果使用了这个模式，则所有和图色相关的函数

均视为对此图片进行处理，比如文字识别
查找图片 颜色 等等一切图色函数.

需要注意的是，设定以后，此图片就已经加入了缓冲，如果更改了源图片内容，那么需要  
释放此缓冲，重新设置.

3.    
"mem:addr,size" 指定输入模式为指定的图片,此图片在内存当中. addr为图像内存地址,size为图像内存大小.  
如果使用了这个模式，则所有和图色相关的函数,均视为对此图片进行处理.  
比如文字识别 查找图片 颜色 等等一切图色函数.

返回值:

整形数:  
0: 失败

1: 成功

示例:

// 设定为默认的模式  
dm\_ret = dm.SetDisplayInput("screen")

// 设定为图片模式 图片采用相对路径模式 相对于SetPath的路径  
dm\_ret = dm.SetDisplayInput("pic:test.bmp")

// 设为图片模式 图片采用绝对路径模式  
dm\_ret = dm.SetDisplayInput("pic:d:\test\test.bmp")

// 设为图片模式 但是每次设置前 先清除缓冲  
dm\_ret = dm.FreePic("test.bmp")  
dm\_ret = dm.SetDisplayInput("pic:test.bmp")

// 设置为图片模式,图片从内存中获取  
dm\_ret = dm.SetDisplayInput("mem:1230434,884")