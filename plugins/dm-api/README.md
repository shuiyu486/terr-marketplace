# dm-api

大漠插件 (DaMao Plugin) API 文档查询 skill，为 Claude Code 提供 465 个大漠插件 API 函数的按需查询能力。

## 功能

- **单函数查询**：输入函数名（如 `dm.FindPic`），返回完整的参数说明、返回值和示例
- **分类浏览**：列出指定分类下的所有函数（如"文字识别"）
- **任务导向查询**：描述需求（如"后台找图点击"），给出完整实现方案

## 覆盖范围

17 个分类，465 个函数：键鼠、图色、文字识别、窗口、后台设置、内存、文件、系统、算法、AI、基本设置、杂项、汇编、答题、防护盾、常见问题、Foobar

## 使用方式

安装后，在 Claude Code 中直接提问即可触发：

- `dm.FindPic 怎么用？`
- `大漠插件有哪些文字识别的函数？`
- `我想在后台找图点击，怎么实现？`
- `BindWindow 的 display 参数 gdi 和 dx2 有什么区别？`

## 结构

```
dm-api/
├── .claude-plugin/plugin.json          # 插件元数据
├── skills/dm-api/SKILL.md              # Skill 定义
├── references/dm_api_docs/             # API 文档（465 个 .md 文件）
│   ├── 键鼠/
│   ├── 图色/
│   ├── 文字识别/
│   ├── 窗口/
│   ├── 后台设置/
│   ├── 内存/
│   └── ...
├── LICENSE
└── README.md
```
