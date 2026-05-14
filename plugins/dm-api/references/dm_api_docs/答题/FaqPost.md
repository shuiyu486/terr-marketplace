函数简介:

发送指定的图像句柄到指定的服务器,并立即返回(异步操作).

函数原型:  
  
long FaqPost(server, handle, request\_type, time\_out)

参数定义:  
  
server 字符串: 服务器地址以及端口,格式为(ip:port),例如
"192.168.1.100:12345"

handle 整形数: 由FaqCapture获取到的句柄

request\_type 整形数: 取值定义如下

            
0 : 要求获取坐标

            
1 : 要求获取选项,比如(ABCDE)

            
2 : 要求获取文字答案

3 : 要求获取N个坐标.此功能要求答题器必须是v15之后的版本.

time\_out 整形数: 表示等待多久,单位是毫秒

返回值:

整形数:  
0 : 失败，一般情况下是由于上个FaqPost还没有处理完毕(服务器还没返回)

1 : 成功

示例:

// 截取这个范围内,静态图片,图像质量为中等50   
handle = dm.FaqCapture(50,50,300,400,50,0,0)  
// 调用FaqPost异步发送  
dm\_ret = dm.FaqPost("192.168.1.100:12345",handle,1,3 \* 60 \* 1000)  
If dm\_ret = 0 Then  
    MessageBox "发送失败，可能上个FaqPost还未处理完毕"  
    EndScript  
End If  
  
// 不影响脚本运行  
Do  
   result = dm.FaqFetch()  
   If len(result) > 0 Then  
       
result = split(result,":")  
        If result(0) =
"OK" Then  
             MessageBox
result(1)  
       
Else  
            
MessageBox "错误:"& result(1)  
       
End If   
   End If  
   // 做其他的事情 这里就假设为延时  
   Delay 1000  
Loop

注 : 从插件版本2.1119之后，接口FaqCapture返回handle，不需要再手动调用FaqRelease释放了。插件已经自动释放了.

本接口不支持多ip发送.