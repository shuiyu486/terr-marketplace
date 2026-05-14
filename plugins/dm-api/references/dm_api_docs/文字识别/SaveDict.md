# SaveDict

**分类:** 文字识别

**签名:** `long SaveDict(index,file)`

**描述:** 保存指定的字库到指定的文件中.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| index | int | 字库索引序号 取值为0-99对应100个字库 |
| file | str | 文件名 |

## 返回值

- 0:失败
- 1:成功

## 示例

```vbs
dm.SetPath "c:\test_game"
dm.AddDict 0,"FFF00A7D49292524A7D402805FFC$回$0.0.54$11"
dm.AddDict 0,"3F0020087FF08270B9A108268708808$收$0.0.43$11"
dm.AddDict 0,"2055C98617420807C097F222447C800$站$0.0.44$11"
dm.SaveDict 0,"test.txt"
```
