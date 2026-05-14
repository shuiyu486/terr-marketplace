# GetSystemInfo

**分类:** 系统

**签名:** `string GetSystemInfo(type,method)`

**描述:** 获取指定的系统信息.

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| type | str | 取值如下 "cpuid" : 表示获取cpu序列号. method可取0和1 "disk_volume_serial id" : 表示获取分区序列号. id表示分区序号. 0表示C盘.1表示D盘.以此类推. 最高取到5. 也就是6个分区. method可取0 "bios_vendor" : 表示获取bios厂商信息. method可取0和1 "bios_version" : 表示获取bios版本信息. method可取0和1 "bios_release_date" : 表示获取bios发布日期. method可取0和1 "bios_oem" : 表示获取bios里的oem信息. method可取0 "board_vendor" : 表示获取主板制造厂商信息. method可取0和1 "board_product" : 表示获取主板产品信息. method可取0和1 "board_version" : 表示获取主板版本信息. method可取0和1 "board_serial" : 表示获取主板序列号. method可取0 "board_location" : 表示获取主板位置信息. method可取0 "system_manufacturer" : 表示获取系统制造商信息. method可取0和1 "system_product" : 表示获取系统产品信息. method可取0和1 "system_serial" : 表示获取bios序列号. method可取0 "system_uuid" : 表示获取bios uuid. method可取0 "system_version" : 表示获取系统版本信息. method可取0和1 "system_sku" : 表示获取系统sku序列号. method可取0和1 "system_family" : 表示获取系统家族信息. method可取0和1 "product_id" : 表示获取系统产品id. method可取0 "system_identifier" : 表示获取系统标识. method可取0 "system_bios_version" : 表示获取系统BIOS版本号. method可取0. 多个结果用"|"连接. "system_bios_date" : 表示获取系统BIOS日期. method可取0 |
| method | int | 获取方法. 一般从0开始取值. |

## 返回值

- 字符串表达的系统信息.

## 示例

```vbs
// 获取系统所有特征信息

TracePrint
dm.GetSystemInfo("cpuid",0)
TracePrint dm.GetSystemInfo("cpuid",1)

TracePrint
dm.GetSystemInfo("bios_vendor",0)
TracePrint dm.GetSystemInfo("bios_vendor",1)
TracePrint dm.GetSystemInfo("bios_version",0)
TracePrint dm.GetSystemInfo("bios_version",1)
TracePrint dm.GetSystemInfo("bios_release_date",0)
TracePrint dm.GetSystemInfo("bios_release_date",1)
TracePrint dm.GetSystemInfo("bios_oem",0)

TracePrint dm.GetSystemInfo("board_vendor",0)
TracePrint dm.GetSystemInfo("board_vendor",1)
TracePrint dm.GetSystemInfo("board_product",0)
TracePrint dm.GetSystemInfo("board_product",1)
TracePrint dm.GetSystemInfo("board_version",0)
TracePrint dm.GetSystemInfo("board_version",1)
TracePrint dm.GetSystemInfo("board_serial",0)
TracePrint dm.GetSystemInfo("board_location",0)

TracePrint
dm.GetSystemInfo("system_manufacturer",0)
TracePrint dm.GetSystemInfo("system_manufacturer",1)
TracePrint dm.GetSystemInfo("system_product",0)
TracePrint dm.GetSystemInfo("system_product",1)
TracePrint dm.GetSystemInfo("system_serial",0)
TracePrint dm.GetSystemInfo("system_uuid",0)
TracePrint dm.GetSystemInfo("system_version",0)
TracePrint dm.GetSystemInfo("system_version",1)
TracePrint dm.GetSystemInfo("system_sku",0)
TracePrint dm.GetSystemInfo("system_sku",1)
TracePrint dm.GetSystemInfo("system_family",0)
TracePrint dm.GetSystemInfo("system_family",1)

TracePrint
dm.GetSystemInfo("product_id",0)
TracePrint dm.GetSystemInfo("system_identifier",0)
TracePrint dm.GetSystemInfo("system_bios_version",0)
TracePrint dm.GetSystemInfo("system_bios_date",0)

TracePrint
dm.GetSystemInfo("disk_volume_serial 0",0)
TracePrint dm.GetSystemInfo("disk_volume_serial 1",0)
TracePrint dm.GetSystemInfo("disk_volume_serial 2",0)

TracePrint dm.GetDiskSerial(0)
TracePrint dm.GetDiskModel(0)
TracePrint dm.GetDiskReversion(0)

TracePrint dm.GetMac()
```
