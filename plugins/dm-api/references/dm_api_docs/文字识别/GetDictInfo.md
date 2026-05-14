# GetDictInfo

**分类:** 文字识别

**签名:** `string GetDictInfo(str,font_name,font_size,flag)`

**描述:** 根据指定的文字，以及指定的系统字库信息，获取字库描述信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| str | str | 需要获取的字符串 |
| font_name | str | 系统字体名,比如"宋体" |
| font_size | int | 系统字体尺寸，这个尺寸一定要以大漠综合工具获取的为准.如何获取尺寸看视频教程. |
| flag | int | 字体类别 取值可以是以下值的组合,比如1+2+4+8,2+4. |

## 返回值

- 返回字库信息,每个字符的字库信息用"|"来分割

## 示例

```vbs
// 下面的代码是获取"回收站"这3个字符的字库信息，然后加入到字库1中.
font_desc = dm.GetDictInfo("回收站","宋体",9,0)
font_desc = split(font_desc,"|")
count = ubound(font_desc)
for i = 0 to count
TracePrint
font_desc(i)
dm.AddDict
1,font_desc(i)
next
```
