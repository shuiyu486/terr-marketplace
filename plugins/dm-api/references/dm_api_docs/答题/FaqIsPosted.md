# FaqIsPosted

**分类:** 答题

**签名:** `long FaqIsPosted()`

**描述:** 用于判断当前对象是否有发送过答题(FaqPost)

## 参数

*此函数无参数。*

## 返回值

- 0 : 没有
- 1 : 有发送过

## 示例

```vbs
// 判断是否已经发过题目了
if dm.FaqIsPosted() = 0 then
// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms
handle =
dm.FaqCapture(50,50,300,400,50,100,3000)
// 调用FaqPost异步发送
dm_ret = dm.FaqPost("192.168.1.100:12345",handle,1,3 \* 60 \* 1000)
If dm_ret = 0 Then
MessageBox "发送失败，可能上个FaqPost还未处理完毕"
EndScript
End If
end if

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
