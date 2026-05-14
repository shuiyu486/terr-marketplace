函数简介:

获取鼠标特征码. 当BindWindow或者BindWindowEx中的mouse参数含有dx.mouse.cursor时，

获取到的是后台鼠标特征，否则是前台鼠标特征.  [关于如何识别后台鼠标特征.](../常见问题/如何可以后台识别鼠标特征码.htm)

函数原型:  
  
string GetCursorShapeEx(int type)

参数定义:

type 整形数:获取鼠标特征码的方式. 和工具中的方式1 方式2对应. 方式1此参数值为0. 方式2此参数值为1.

返回值:

字符串:  
成功时，返回鼠标特征码.    
失败时，返回空的串.

示例:

mouse\_tz = dm.GetCursorShapeEx(0)  
If mouse\_tz = "7d7160fe" Then  
    MessageBox
"找到特征码"  
End If

注: 当type为0时，和GetCursorShape等效.  
另要特别注意,WIN7以及以上系统，必须在字体显示设置里把文字大小调整为默认(100%),否则特征码会变.如图所示.