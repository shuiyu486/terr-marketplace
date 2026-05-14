函数简介:

获取指定的系统信息.

函数原型:  
  
string GetSystemInfo(type,method)

参数定义:

type 字符串: 取值如下  
            
"cpuid" : 表示获取cpu序列号. method可取0和1  
            
"disk\_volume\_serial id" : 表示获取分区序列号.
id表示分区序号. 0表示C盘.1表示D盘.以此类推. 最高取到5. 也就是6个分区. method可取0  
            
"bios\_vendor" : 表示获取bios厂商信息. method可取0和1  
            
"bios\_version" : 表示获取bios版本信息. method可取0和1  
            
"bios\_release\_date" : 表示获取bios发布日期. method可取0和1  
            
"bios\_oem" : 表示获取bios里的oem信息. method可取0  
            
"board\_vendor" : 表示获取主板制造厂商信息. method可取0和1  
            
"board\_product" : 表示获取主板产品信息. method可取0和1  
            
"board\_version" : 表示获取主板版本信息. method可取0和1  
            
"board\_serial" : 表示获取主板序列号. method可取0  
            
"board\_location" : 表示获取主板位置信息. method可取0  
            
"system\_manufacturer" : 表示获取系统制造商信息.
method可取0和1  
            
"system\_product" : 表示获取系统产品信息. method可取0和1  
            
"system\_serial" : 表示获取bios序列号. method可取0  
            
"system\_uuid" : 表示获取bios uuid. method可取0  
            
"system\_version" : 表示获取系统版本信息. method可取0和1  
            
"system\_sku" : 表示获取系统sku序列号. method可取0和1  
            
"system\_family" : 表示获取系统家族信息. method可取0和1  
            
"product\_id" : 表示获取系统产品id. method可取0  
            
"system\_identifier" : 表示获取系统标识. method可取0  
            
"system\_bios\_version" : 表示获取系统BIOS版本号. method可取0. 多个结果用"|"连接.  
            
"system\_bios\_date" : 表示获取系统BIOS日期. method可取0

method整形数: 获取方法. 一般从0开始取值.

返回值:

字符串:  
字符串表达的系统信息.

示例:

// 获取系统所有特征信息

TracePrint
dm.GetSystemInfo("cpuid",0)  
TracePrint dm.GetSystemInfo("cpuid",1)

TracePrint
dm.GetSystemInfo("bios\_vendor",0)  
TracePrint dm.GetSystemInfo("bios\_vendor",1)  
TracePrint dm.GetSystemInfo("bios\_version",0)  
TracePrint dm.GetSystemInfo("bios\_version",1)  
TracePrint dm.GetSystemInfo("bios\_release\_date",0)  
TracePrint dm.GetSystemInfo("bios\_release\_date",1)  
TracePrint dm.GetSystemInfo("bios\_oem",0)

TracePrint dm.GetSystemInfo("board\_vendor",0)  
TracePrint dm.GetSystemInfo("board\_vendor",1)  
TracePrint dm.GetSystemInfo("board\_product",0)  
TracePrint dm.GetSystemInfo("board\_product",1)  
TracePrint dm.GetSystemInfo("board\_version",0)  
TracePrint dm.GetSystemInfo("board\_version",1)  
TracePrint dm.GetSystemInfo("board\_serial",0)  
TracePrint dm.GetSystemInfo("board\_location",0)

TracePrint
dm.GetSystemInfo("system\_manufacturer",0)  
TracePrint dm.GetSystemInfo("system\_manufacturer",1)  
TracePrint dm.GetSystemInfo("system\_product",0)  
TracePrint dm.GetSystemInfo("system\_product",1)  
TracePrint dm.GetSystemInfo("system\_serial",0)  
TracePrint dm.GetSystemInfo("system\_uuid",0)  
TracePrint dm.GetSystemInfo("system\_version",0)  
TracePrint dm.GetSystemInfo("system\_version",1)  
TracePrint dm.GetSystemInfo("system\_sku",0)  
TracePrint dm.GetSystemInfo("system\_sku",1)  
TracePrint dm.GetSystemInfo("system\_family",0)  
TracePrint dm.GetSystemInfo("system\_family",1)

TracePrint
dm.GetSystemInfo("product\_id",0)  
TracePrint dm.GetSystemInfo("system\_identifier",0)  
TracePrint dm.GetSystemInfo("system\_bios\_version",0)  
TracePrint dm.GetSystemInfo("system\_bios\_date",0)

TracePrint
dm.GetSystemInfo("disk\_volume\_serial 0",0)  
TracePrint dm.GetSystemInfo("disk\_volume\_serial 1",0)  
TracePrint dm.GetSystemInfo("disk\_volume\_serial 2",0)

TracePrint dm.GetDiskSerial(0)  
TracePrint dm.GetDiskModel(0)  
TracePrint dm.GetDiskReversion(0)

TracePrint dm.GetMac()