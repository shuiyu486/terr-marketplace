# EnableMouseAccuracy

**分类:** 键鼠

**签名:** `long EnableMouseAccuracy(enable)`

**描述:** 设置当前系统鼠标的精确度开关. 如果所示。 此接口仅仅对前台MoveR接口起作用.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| enable | int | 0 关闭指针精确度开关.  1打开指针精确度开关. 一般推荐关闭. |

## 返回值

- 设置之前的精确度开关.

## 示例

```vbs
dm.SetMouseAccuracy 0
```
