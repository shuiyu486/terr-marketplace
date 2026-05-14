# CreateFoobarCustom

**分类:** Foobar

**签名:** `long CreateFoobarCustom(hwnd,x,y,pic_name,trans_color,sim)`

**描述:** 根据指定的位图创建一个自定义形状的窗口

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| hwnd | int | 指定的窗口句柄,如果此值为0,那么就在桌面创建此窗口 |
| x | int | 左上角X坐标(相对于hwnd客户区坐标) |
| y | int | 左上角Y坐标(相对于hwnd客户区坐标) |
| pic_name | str | 位图名字. [如果第一个字符是@,则采用指针方式. @后面是指针地址和大小. 必须是十进制](mailto:如果第一个字符是@,则采用指针方式.%20@后面是指针地址和大小.%20必须是十进制). 具体看下面的例子 |
| trans_color | str | 透明色(RRGGBB) |
| sim | double | 透明色的相似值 0.1-1.0 |

## 返回值

- 整形数 : 创建成功的窗口句柄

## 示例

```vbs
foobar = dm.CreateFoobarCustom(hwnd,10,10,"菜单.bmp","FF00FF",1.0)

foobar = dm.CreateFoobarCustom(hwnd,10,10,"@9237392578,2345","FF00FF",1.0)
```

## 注意

- foobar不能在本进程窗口内创建.
