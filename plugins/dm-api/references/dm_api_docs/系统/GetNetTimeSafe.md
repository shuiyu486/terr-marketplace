# GetNetTimeSafe

**分类:** 系统

**签名:** `string GetNetTimeSafe()`

**描述:** 服务器压力太大,此函数不再支持。 请使用GetNetTimeByIp

## 参数

*此函数无参数。*

## 返回值

- 时间格式. 和now返回一致. 比如"2001-11-01
- 23:14:08"

## 示例

```vbs
t = dm.GetNetTimeSafe()
TracePrint "当前北京时间是:"&t
```

## 注意

- 此接口不支持简单游平台.
- 如果程序无法访问时间服务器，那么空串.
