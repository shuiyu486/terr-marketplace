# FaqSend

**分类:** 答题

**签名:** `string FaqSend(server, handle, request_type, time_out)`

**描述:** 发送指定的图像句柄到指定的服务器,并等待返回结果(同步等待).

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| server | str | 服务器地址以及端口,格式为(ip:port),例如 "192.168.1.100:12345" 多个地址可以用"|"符号连接。比如"192.168.1.100:12345|192.168.1.101:12345"。 |
| handle | int | 由FaqCapture获取到的句柄 |
| request_type | int | 取值定义如下 |
| time_out | int | 表示等待多久,单位是毫秒 |

## 返回值

- 如果此函数调用失败,那么返回值如下 "Error:错误描述" 如果函数调用成功,那么返回值如下 "OK:答案" 根据request\_type取值的不同,返回值不同 当request\_type 为0时,答案的格式为"x,y" (不包含引号) 当request\_type 为1时,答案的格式为"1" "2" "3" "4" "5" "6" (不包含引号) 当request\_type 为2时,答案就是要求的答案 比如 "李白" (不包含引号) 当request\_type 为3时,答案的格式为"x1,y1|...|xn,yn|" 比如 "20,30|78,68|33,33" (不包含引号)

## 示例

```vbs
// 截取这个范围内,3秒动画,图像质量为中等50,动画帧率间隔为100ms
handle = dm.FaqCapture(20,20,100,100,50,100,3000)
// 等待3分钟,答案要求是选项
result =
dm.FaqSend("192.168.1.100:12345|192.168.1.101:12345",handle,1,3 \* 60
\* 1000)

result = split(result,":")
If result(0) = "OK" Then
If result(1) = "1"
Then
MessageBox "1"
ElseIf result(1) =
"2" Then
MessageBox
"2"
ElseIf result(1) =
"3" Then
MessageBox
"3"
ElseIf result(1) =
"4" Then
MessageBox
"4"
End If
Else
MessageBox "错误:"& result(1)
End If

注 : 从插件版本2.1119之后，接口FaqCapture返回handle，不需要再手动调用FaqRelease释放了。插件已经自动释放了.

另外，当向多个地址发送题目时，只要有任意一个服务器返回答案，函数就返回结果。
```
