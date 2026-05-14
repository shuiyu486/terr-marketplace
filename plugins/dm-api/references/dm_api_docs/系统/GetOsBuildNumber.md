函数简介:

得到操作系统的build版本号.  比如win10 16299,那么返回的就是16299. 其他类似

函数原型:  
  
long GetOsBuildNumber()

参数定义:

返回值:

整形数:  
build 版本号  
失败返回0

示例:

os\_build\_number = dm.GetOsBuildNumber()  
  
WIN11的BuildNumber从22000开始. 如果要判断是不是WIN11,直接判断BuildNumber是否大于等于22000即可.