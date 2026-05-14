# SetExcludeRegion

**分类:** 图色

**签名:** `long SetExcludeRegion(mode,info)`

**描述:** 设置图色,以及文字识别时,需要排除的区域.(支持所有图色接口,以及文字相关接口,但对单点取色,或者单点颜色比较的接口不支持)

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| mode | int | 模式,取值如下: |
| info | str | 根据mode的取值来决定 当mode为0时,此参数指添加的区域,可以多个区域,用"|"相连. 格式为"x1,y1,x2,y2|....." 当mode为1时,此参数为排除区域的颜色,"RRGGBB" 当mode为2时,此参数无效 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
// 先清空区域
dm.SetExcludeRegion 2,""

// 添加区域
dm.SetExcludeRegion 0,"30,30,100,300|300,400,500,600"
dm.SetExcludeRegion 0,"100,100,200,200"

至于颜色如果有需要也可以设置比如
dm.SetExcludeRegion 1,"FF11FF"
```
