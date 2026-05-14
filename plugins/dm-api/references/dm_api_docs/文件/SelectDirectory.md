# SelectDirectory

**分类:** 文件

**签名:** `string SelectDirectory()`

**描述:** 弹出选择文件夹对话框，并返回选择的文件夹.

## 参数

*此函数无参数。*

## 返回值

- 选择的文件夹全路径

## 示例

```vbs
TracePrint dm.SelectDirectory()

*注:此接口要求当前线程的COM模型必须是STA. 如果当前对象创建于非STA的线程,那么调用此接口有可能会导致程序崩溃.*具体的示例,可以查看类库生成工具里产生的例子.
```
