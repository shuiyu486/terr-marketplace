# SetScreen

**分类:** 系统

**签名:** `long SetScreen(width,height,depth)`

**描述:** 设置系统的分辨率 系统色深

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| width | int | 屏幕宽度 |
| height | int | 屏幕高度 |
| depth | int | 系统色深 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
dm_ret = dm.SetScreen(1024,768,16)
```
