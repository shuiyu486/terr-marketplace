# FaqCancel

**分类:** 答题

**签名:** `long FaqCancel()`

**描述:** 可以把上次FaqPost的发送取消,接着下一次FaqPost

## 参数

*此函数无参数。*

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
// 调用FaqPost异步发送，必须先取消,否则FaqCapture会因为上一次FaqPost未处理完毕而失败.
dm.FaqCancel
// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms
handle = dm.FaqCapture(50,50,300,400,50,100,3000)
dm_ret = dm.FaqPost("192.168.1.100:12345",handle,1,3 \* 60 \* 1000)
If dm_ret = 0 Then
MessageBox "发送失败，可能上个FaqPost还未处理完毕"
EndScript
End If

// 不影响脚本运行
Do
result = dm.FaqFetch()
If len(result) > 0 Then

MessageBox "服务器返回结果 = "&result
End If
// 做其他的事情 这里就假设为延时
Delay 1000
Loop
```
