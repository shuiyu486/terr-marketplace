# ForceUnBindWindow

**分类:** 后台设置

**签名:** `long ForceUnBindWindow(hwnd)`

**描述:** 强制解除绑定窗口,并释放系统资源.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 需要强制解除绑定的窗口句柄. |

## 返回值

- 0: 失败
- 1: 成功

## 示例

```vbs
dm_ret = dm.ForceUnBindWindow(hwnd)
```

## 注意

- 此接口一般用在BindWindow和BindWindowEx中，使用了模式1 3 5 7或者属性dx.public.hide.dll后，在线程或者进程结束后，没有正确调用UnBindWindow而导致下次绑定无法成功时，可以先调用这个函数强制解除绑定，并释放资源，再进行绑定.
- 此接口不可替代UnBindWindow. 只是用在非常时刻. 切记.
- 一般情况下可以无条件的在BindWindow或者BindWindowEx之前调用一次此函数。保证此刻窗口处于非绑定状态.
- 另外，需要注意的是,此函数只可以强制解绑在同进程绑定的窗口.  不可在不同的进程解绑别的进程绑定的窗口.(会产生异常)
