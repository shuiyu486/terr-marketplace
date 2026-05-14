函数简介:

保存指定的字库到指定的文件中.

函数原型:  
  
long SaveDict(index,file)

参数定义:  
  
index 整形数:字库索引序号 取值为0-99对应100个字库  
file 字符串:文件名

返回值:

整形数:  
0:失败  
1:成功

示例:

dm.SetPath "c:\test\_game"  
dm.AddDict 0,"FFF00A7D49292524A7D402805FFC$回$0.0.54$11"  
dm.AddDict 0,"3F0020087FF08270B9A108268708808$收$0.0.43$11"  
dm.AddDict 0,"2055C98617420807C097F222447C800$站$0.0.44$11"  
dm.SaveDict 0,"test.txt"