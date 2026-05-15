# config-sync

终端配置文件双向同步与兼容性检查。在本地环境（`~/`）和 [ccNovaTerm](https://github.com/shuiyu486/ccNovaTerm) 项目之间同步、对比、快速检查配置兼容性。

## 功能

- **双向同步**：本地 → 项目（push）或 项目 → 本地（pull）
- **完整对比**：逐文件展示本地与项目模板的差异
- **快速兼容检查**：基于 hash 的轻量级检测，无需远程获取，秒级完成
- **自动备份**：同步前自动备份现有配置文件
- **代理保护**：`env.nu` 的 `load-env` 代理行自动保护，不被覆盖
- **自定义排除**：支持 `~/.configsyncignore` 定义额外排除规则

## 管理范围

| 本地路径 | 说明 |
|---------|------|
| `~/.wezterm.lua` | WezTerm 终端配置 |
| `~\AppData\Roaming\nushell\config.nu` | Nushell 主配置 |
| `~\AppData\Roaming\nushell\env.nu` | Nushell 环境变量 |
| `~/.config/starship.toml` | Starship 提示符配置 |
| `~/.claude/statusline.ps1` | Claude Code 状态栏 |
| `~/.claude/settings.json` | Claude Code 设置 |
| `<项目根>/CLAUDE.local.md` | 项目级 CLAUDE 指令 |

## 使用方式

安装后，在 Claude Code 中直接表达意图即可触发：

- `同步到项目` / `push configs` — 将本地配置推送到 ccNovaTerm
- `同步到本地` / `pull configs` — 从 ccNovaTerm 拉取配置到本地
- `对比` / `diff` / `有什么不同` — 查看配置差异
- `快速检查` / `兼容吗` — hash 级兼容性检查

## 结构

```
config-sync/
├── .claude-plugin/plugin.json      # 插件元数据
├── skills/config-sync/
│   ├── SKILL.md                    # Skill 定义（渐进式披露架构）
│   ├── references/                 # 8 个参考文件（按需加载）
│   │   ├── diff.md                 # 完整对比流程
│   │   ├── encoding.md             # UTF-8 编码安全
│   │   ├── exclusions.md           # 排除规则
│   │   ├── paths.md                # 路径解析
│   │   ├── placeholders.md         # 占位符处理
│   │   ├── quick-check.md          # 快速检查流程
│   │   ├── sync-pull.md            # 拉取同步流程
│   │   └── sync-push.md            # 推送同步流程
│   └── scripts/
│       └── verify.ps1              # 验证脚本
└── README.md
```

## 要求

- Windows (PowerShell 5.1+)
- 支持本地项目和远程 GitHub 获取
