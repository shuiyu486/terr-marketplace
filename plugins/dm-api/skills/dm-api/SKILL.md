---
name: dm-api
description: 查询大漠插件(DaMao Plugin) API 文档。当用户询问大漠插件函数用法、按键精灵脚本编写、找图找色、后台绑定、内存读写、文字识别、窗口操作等相关问题时使用此 skill。即使用户没有明确提到"大漠"，只要涉及 dm.FindPic、dm.BindWindow、dm.Ocr 等以 dm. 开头的函数调用，或者询问如何在按键精灵中实现自动化操作（找图、找色、找字、后台、内存），都应触发此 skill。
version: 1.0.0
---

# 大漠插件 API 文档查询

大漠插件是按键精灵等自动化工具的核心 COM 组件，提供键鼠模拟、图色查找、文字识别、窗口管理、内存读写等功能。

## 文档位置

所有 API 文档在本 skill 的 `references/dm_api_docs/` 目录下，按功能分类存放为 Markdown 文件。共 465 个函数文档，覆盖 17 个分类。

**不要一次性读取所有文档**，按需查找即可。

## 查询流程

### 1. 查询特定函数

用户提到具体函数名时（如 FindPic、BindWindow、Ocr）：

1. 用 Grep 在 `references/dm_api_docs/` 中搜索函数名，定位到对应的 .md 文件
2. Read 该文件获取完整文档
3. 用中文向用户解释函数的用途、参数、返回值和示例

注意：函数名可能出现在多个分类中（如 FindPic 在 图色/ 和 Ai/ 都有），优先读取与用户上下文最相关的分类。如果用户没有明确上下文，优先选择主要分类（图色/ > Ai/，键鼠/ > 后台设置/ 等）。

### 2. 按分类浏览

用户询问某个功能类别时（如"有哪些找图函数"）：

1. 根据下方分类表确定目录
2. 用 Glob 列出 `references/dm_api_docs/<分类>/` 下的 .md 文件
3. 汇总函数列表返回给用户

### 3. 任务导向查询

用户描述要实现的功能（如"怎么在屏幕上找图"、"如何后台操作窗口"）：

1. 根据功能描述判断涉及哪些分类
2. 读取相关函数的文档
3. 给出完整的实现方案，包括推荐函数、参数配置和代码示例

## 分类速查表

| 目录 | 功能 | 典型场景 |
|------|------|----------|
| `键鼠/` | 键盘鼠标模拟 | 点击、移动、按键、滚轮 |
| `图色/` | 找图找色截图 | FindPic、FindColor、Capture |
| `文字识别/` | OCR 文字识别 | FindStr、Ocr、字库管理 |
| `窗口/` | 窗口查找与操作 | FindWindow、EnumWindow、SendString |
| `后台设置/` | 后台绑定与配置 | BindWindow、UnBindWindow、模式设置 |
| `内存/` | 进程内存读写 | ReadInt、WriteString、内存搜索 |
| `文件/` | 文件与 INI 操作 | ReadFile、WriteIni |
| `系统/` | 系统信息与控制 | GetTime、GetMachineCode、SetScreen |
| `算法/` | 坐标与加密 | FindNearestPos、ExcludePos |
| `Ai/` | AI 找图与 YOLO | AiFindPic、AiYoloDetectObjects |
| `基本设置/` | 插件注册与路径 | Reg、SetPath、Ver |
| `杂项/` | 输入法与临界区 | ActiveInputMethod、EnterCri |
| `汇编/` | 汇编代码执行 | AsmAdd、AsmCall |
| `答题/` | 答题系统 | FaqPost、FaqFetch |
| `防护盾/` | 反检测保护 | DmGuard、DmGuardParams |
| `常见问题/` | FAQ | 注册、绑定、兼容性问题 |
| `Foobar/` | 透明窗口绘制 | CreateFoobarRect、FoobarDrawText |

## 输出规范

- 始终用中文回复
- 引用函数时标注分类来源，如 `图色/FindPic`
- 提供代码示例时使用 VBS/按键精灵语法
- 如果函数有多个模式或复杂参数，重点说明常用模式和注意事项
- 当用户的问题涉及多个函数协作时（如"后台找图"需要先 BindWindow 再 FindPic），给出完整流程