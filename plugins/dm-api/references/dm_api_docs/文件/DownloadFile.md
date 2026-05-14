函数简介:

从internet上下载一个文件.

函数原型:  
  
long DownloadFile(url,save\_file,timeout)

参数定义:

url 字符串: 下载的url地址.

save\_file 字符串: 要保存的文件名.

timeout整形数: 连接超时时间，单位是毫秒.

返回值:  
  
整形数:  
1 : 成功  
-1 : 网络连接失败  
-2 : 写入文件失败

示例:  
  
dm.DownloadFile "www.sohu.com","sohu.html",3000

dm.DownloadFile "http://www.sohu.com","d:\sohu.html",3000