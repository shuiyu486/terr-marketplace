# skills2ccPlugin

将 skill 目录转换为 terr-marketplace 可安装插件并发布。

## 功能

- **自动提取元数据**：从 SKILL.md 的 YAML frontmatter 读取 name、description
- **生成 plugin.json**：自动创建符合 marketplace 规范的插件清单
- **组织目录结构**：将源 skill 的所有资源（SKILL.md、references、scripts、agents、assets 等）复制到 `plugins/<name>/skills/<name>/` 下
- **注册 marketplace.json**：以 git-subdir 格式追加到市场注册表
- **验证 + 提交推送**：运行 `claude plugin validate` 并提交推送

## 使用方式

安装后，在 Claude Code 中表达发布意图即可触发：

- `发布这个 skill 到 marketplace`
- `打包插件`
- `把这个注册到 terr-marketplace`
- `让这个 skill 能通过 /plugin install 安装`

## 目标目录结构

```
源 skill/                         →    plugins/<name>/
├── SKILL.md                      →    ├── .claude-plugin/
├── references/                   →    │   └── plugin.json
├── scripts/                      →    └── skills/
├── agents/                       →        └── <name>/
├── assets/                       →            ├── SKILL.md
└── ...                           →            ├── references/
                                               ├── scripts/
                                               ├── agents/
                                               └── ...
```

## 结构

```
skills2ccPlugin/
├── .claude-plugin/plugin.json    # 插件元数据
├── skills/skills2ccPlugin/
│   └── SKILL.md                  # Skill 定义（完整操作流程）
└── README.md
```

## 重要说明

- marketplace 使用 **git-subdir** 格式（用户安装时无需 `--sparse` 参数）
- 源 skill 的**所有**子目录都会被复制，不限于 references/ 和 scripts/
- 不修改 marketplace.json 中已有的其他插件条目
