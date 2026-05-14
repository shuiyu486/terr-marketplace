# FoobarSetTrans

**分类:** Foobar

**签名:** `long FoobarSetTrans(hwnd,is_trans,color,sim)`

**描述:** 设置指定Foobar窗口的是否透明

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的Foobar窗口句柄,此句柄必须是通过CreateFoobarxxx创建而来 |
| is_trans | int | 是否透明. 0为不透明(此时,color和sim无效)，1为透明. |
| color | str | 透明色(RRGGBB) |
| sim | double | 透明色的相似值 0.1-1.0 |

## 返回值

- 0 : 失败
- 1 : 成功

## 示例

```vbs
foobar=dm.CreateFoobarRoundRect(hwnd,1,1,300,300,100,100)

dm_ret = dm.FoobarSetFont(foobar,"宋体",50,0)

dm.FoobarSetTrans foobar,1,"000000",1.0

do

dm_ret = dm.FoobarFillRect(foobar,0,0,300,300,"000000")

dm_ret = dm.FoobarDrawText(foobar,0,0,300,100,"测试","FF0000",1)

dm.foobarupdate foobar

delay 100

Loop

EndScript
```

## 注意

- 调用此接口，最好打开windows的dwm. 否则可能会卡.
