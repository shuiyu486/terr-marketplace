---
name: dm-api
description: 查询大漠插件(DaMao Plugin) 465 个 API 函数的用法、参数、返回值和示例。
disable-model-invocation: true
version: 1.1.0
---

# 大漠插件 API 文档查询

大漠插件是按键精灵/TC/易语言等自动化工具的核心 COM 组件，提供键鼠模拟、图色查找、文字识别、窗口管理、内存读写等功能。

## 快速定位函数

**首选方案：查阅函数索引**

`references/functions_index.json` 包含全部 465 个函数的索引，每个条目有函数名、分类、签名、描述和参数列表。当你需要：
- 快速确认某个函数是否存在
- 了解有哪些相关函数（如"所有找图相关的函数"）
- 按分类浏览函数列表

用 Grep 搜索索引文件是最快的方式：
```
Grep pattern="FindPic" path="references/functions_index.json" output_mode="content"
```

**备选方案：直接搜索文档**

当索引中没有你需要的信息时，再深入到具体分类目录的 .md 文件中搜索。

## 文档格式说明

每个函数的 .md 文档使用统一的结构化格式：

```
# 函数名
**分类:** 分类名
**签名:** `返回类型 函数名(参数列表)`
**描述:** 一句话功能说明

## 参数
| 参数 | 类型 | 说明 |    ← 表格形式，可直接获取参数名/类型/含义

## 返回值                              ← 枚举格式，列出所有可能的返回值及含义

## 示例                                ← VBS 代码块
## 注意                                ← （可选）使用注意事项
```

**阅读策略：** 大多数查询只需看"签名 + 描述 + 参数表"三部分即可回答。仅在用户需要代码示例或遇到错误时才读"示例"和"注意"。

## 查询流程

### 1. 查询特定函数

用户提到具体函数名时（如 FindPic、BindWindow、Ocr、ReadInt）：

1. **首选**：用 Grep 在 `references/functions_index.json` 中搜索函数名，获取分类和签名
2. Read 对应分类目录下的 .md 文件（如 `references/dm_api_docs/图色/FindPic.md`）
3. 解析结构化格式：签名行 → 参数表 → 返回值列表
4. 用中文向用户解释函数用途、参数含义、返回值和典型示例

### 2. 按功能类别浏览

用户询问某个功能领域时（如"有哪些找图函数"、"后台绑定相关函数"）：

1. 用 Grep 在 `references/functions_index.json` 的 `"categories"` 字段中查看该分类的函数列表
2. 汇总函数名列表，按功能相似度排序推荐
3. 如用户对某个具体函数感兴趣，再 Read 该函数的 .md 文档

### 3. 任务导向查询（多函数协作）

用户描述要实现的功能（如"后台找图点击"、"内存读取血量"）：

1. 分析任务涉及的功能域（窗口→绑定→图色→键鼠 / 窗口→绑定→内存）
2. 在索引中确认相关函数的完整列表
3. 按执行顺序逐个读取关键函数的文档
4. 给出完整实现方案：推荐函数 → 参数配置要点 → 代码示例 → 常见陷阱

**典型协作模式：**
- 后台找图点击：BindWindow/BindWindowEx → FindPic/FindPicEx → MoveTo → LeftClick
- 后台找字点击：BindWindow → FindStr/FindStrFast → MoveTo → LeftClick
- 后台截图识别：BindWindow → Capture → Ocr
- 内存读取数值：BindWindow → SetMemoryHwndAsProcessId → ReadInt/ReadFloat
- AI 找图：LoadAi/LoadAiMemory → AiFindPic/AiFindPicEx

## 分类速查表

| 目录 | 功能 | 关键函数 | 典型场景 |
|------|------|----------|----------|
| `键鼠/` | 键盘鼠标模拟 | MoveTo, LeftClick, KeyPress | 点击、移动、拖拽、按键 |
| `图色/` | 找图找色截图 | FindPic, FindColor, Capture | 图像匹配、颜色判断、截图 |
| `文字识别/` | OCR 文字识别 | FindStr, Ocr, FindStrFast | 识别屏幕文字、找字 |
| `窗口/` | 窗口查找与操作 | FindWindow, EnumWindow | 窗口句柄获取、枚举 |
| `后台设置/` | 后台绑定与配置 | BindWindow, BindWindowEx | 后台自动化、绑定模式选择 |
| `内存/` | 进程内存读写 | ReadInt, WriteString, FindData | 读取血量/蓝量、修改内存 |
| `文件/` | 文件与 INI 操作 | ReadFile, WriteIni | 配置文件读写 |
| `系统/` | 系统信息与控制 | GetTime, GetMachineCode | 延时、机器码、系统状态 |
| `算法/` | 坐标与加密 | FindNearestPos, ExcludePos | 坐标过滤、智能寻路 |
| `Ai/` | AI 找图与 YOLO | AiFindPic, AiYoloDetectObjects | AI 图像识别、YOLO 检测 |
| `基本设置/` | 插件注册与路径 | Reg, SetPath, Ver | 注册插件、工作目录 |
| `杂项/` | 输入法与临界区 | ActiveInputMethod, EnterCri | 输入法切换、临界区保护 |
| `汇编/` | 汇编代码执行 | AsmAdd, AsmCall | 远程汇编注入 |
| `答题/` | 答题系统 | FaqPost, FaqFetch | 远程答题、验证码识别 |
| `防护盾/` | 反检测保护 | DmGuard, DmGuardParams | 反检测、隐藏保护 |
| `常见问题/` | FAQ | 注册、绑定、兼容性 | 问题排查、兼容性 |
| `Foobar/` | 透明窗口绘制 | CreateFoobarRect, FoobarDrawText | 透明信息叠加显示 |

## 输出规范

- 始终用中文回复
- 引用函数时标注分类来源，如 `图色/FindPic`、`后台设置/BindWindow`
- 提供代码示例时使用 VBS/按键精灵语法
- 参数类型简写：int(整形数)、str(字符串)、double(双精度浮点数)、long(长整形数)、int*(变参指针/输出参数)
- 当函数有多种模式或复杂参数时，重点说明常用模式和注意事项
- 当用户的问题涉及多个函数协作时，给出完整执行流程和顺序
- 涉及后台操作时，提醒用户必须先 BindWindow 再进行后续操作
- 涉及内存操作时，提醒用户需要先绑定窗口并注意 SetMemoryHwndAsProcessId 的设置
