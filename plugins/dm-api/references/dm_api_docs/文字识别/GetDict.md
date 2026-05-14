函数简介:

获取指定字库中指定条目的字库信息.

函数原型:  
  
string GetDict(index,font\_index)

参数定义:  
  
index 整形数: 字库序号(0-99)  
font\_index 整形数: 字库条目序号(从0开始计数,数值不得超过指定字库的字库上限,具体参考[GetDictCount](GetDictCount.htm))

返回值:

字符串:  
返回字库条目信息. 失败返回空串.

示例:

s = dm.GetDict(0,1245)  
TracePrint s  
s = dm.GetDict(1,678)  
TracePrint s