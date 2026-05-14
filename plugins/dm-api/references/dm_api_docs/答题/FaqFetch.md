函数简介:

获取由FaqPost发送后，由服务器返回的答案.

函数原型:  
  
string FaqFetch()

参数定义:

返回值:

字符串:  
如果此函数调用失败,那么返回值如下

"Error:错误描述"

如果函数调用成功,那么返回值如下

"OK:答案"

根据FaqPost中 request\_type取值的不同,返回值不同

当request\_type 为0时,答案的格式为"x,y" (不包含引号)

当request\_type 为1时,答案的格式为"1" "2" "3" "4"
"5" "6" (不包含引号)

当request\_type 为2时,答案就是要求的答案
比如 "李白" (不包含引号)

当request\_type 为3时,答案的格式为"x1,y1|..|xn,yn" 比如
"20,30|78,68|33,33" (不包含引号)

如果返回为空字符串，表示FaqPost还未处理完毕,或者没有调用过FaqPost.

示例:

// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms  
handle = dm.FaqCapture(50,50,300,400,50,100,3000)  
// 调用FaqPost异步发送  
dm\_ret = dm.FaqPost("192.168.1.100:12345",handle,1,3
\* 60 \* 1000)  
If dm\_ret = 0 Then  
    MessageBox
"发送失败，可能上个FaqPost还未处理完毕"  
    EndScript  
End If  
  
// 不影响脚本运行  
Do  
   result = dm.FaqFetch()  
   If len(result)
> 0 Then  
       
MessageBox "服务器返回结果 = "&result  
   End If  
   // 做其他的事情 这里就假设为延时  
   Delay 1000  
Loop

注: 如果此函数调用成功后，插件内部状态会再次重置为未处理状态，可以接着处理FaqPost接口.