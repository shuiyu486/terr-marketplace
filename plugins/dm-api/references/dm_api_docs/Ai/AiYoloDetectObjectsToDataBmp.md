# AiYoloDetectObjectsToDataBmp

**分类:** Ai

**签名:** `long AiYoloDetectObjectsToDataBmp(x1, y1, x2, y2,prob,iou,data,size,mode)`

**描述:** 需要先加载Ai模块. 在指定范围内检测对象,把结果输出到BMP图像数据.用于二次开发.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| x1 | int | 区域的左上X坐标 |
| y1 | int | 区域的左上Y坐标 |
| x2 | int | 区域的右下X坐标 |
| y2 | int | 区域的右下Y坐标 |
| prob | double | **:** 置信度,也可以认为是相似度. 超过这个prob的对象才会被检测 |
| iou | double | **:** 用于对多个检测框进行合并.  越大越不容易合并(很多框重叠). 越小越容易合并(可能会把正常的框也给合并). 所以这个值一般建议0.4-0.6之间. 可以在Yolo综合工具里进行测试. |
| data | int* | 返回图片的数据指针 |
| size | int* | 返回图片的数据长度 |
| mode | int | 0表示绘制的文字信息里包含置信度. 1表示不包含. |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
以下是在E语言中的示例.

.局部变量 data, 整数型

.局部变量 size, 整数型

dm.数值方法 (“AiYoloDetectObjectsToDataBmp”, 0, 0, 100,
200,0.5,0.45, data, size,0)

图片框1.图片 ＝ 指针到字节集 (data, size)
```

## 注意

- 模块内部是全局的,所以调用此接口时得确保没有其它接口去访问此模型.
- 如果多个线程里,UseModel的序号是相同的,那么如果同时执行此接口时,会排队执行.
