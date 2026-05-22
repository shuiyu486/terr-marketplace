# Release

`hook-terr` 通过 `terr-marketplace` 统一分发。

## 文件范围

发布源包括：

- `plugins/hook-terr/.claude-plugin/plugin.json`
- `plugins/hook-terr/hooks/`
- `plugins/hook-terr/core/`
- `plugins/hook-terr/notifiers/`
- `plugins/hook-terr/defaults/`
- `plugins/hook-terr/presets/`
- `plugins/hook-terr/examples/`
- `plugins/hook-terr/references/`
- `plugins/hook-terr/CLAUDE.local.md`
- `plugins/hook-terr/README.md`

## Marketplace 注册

根 `.claude-plugin/marketplace.json` 中必须存在 `hook-terr` 条目，且：

- `source.source` 是 `git-subdir`
- `source.url` 指向 `https://github.com/shuiyu486/terr-marketplace.git`
- `source.path` 是 `plugins/hook-terr`
- version 与插件 `plugin.json` 同步

## 验证

在 marketplace 根目录运行：

```bash
claude plugin validate .
```

发布前查看：

```bash
git status
```

不要自动 commit、push，除非用户明确要求。
