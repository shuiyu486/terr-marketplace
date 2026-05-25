# 发布与副本同步

维护者修改用户可见行为、`src/`、`commands/`、`references/` 或插件元数据时阅读本文件。终端用户只需使用 `/cc-statusline:update`。

## 版本 bump 规则

- bugfix / 文档修正 / reference 路由优化：patch
- 新功能或用户可见配置项：minor
- 破坏性变更：major

版本必须同步到四处：
1. `plugins/cc-statusline/package.json`
2. `plugins/cc-statusline/package-lock.json`
3. `plugins/cc-statusline/.claude-plugin/plugin.json`
4. terr-marketplace 根 `.claude-plugin/marketplace.json` 中的 cc-statusline 条目

不 bump 版本时，`/cc-statusline:update` 可能无法识别更新。

## 验证

```bash
npm run build
echo '{...}' | node dist/index.js
claude plugin validate <terr-marketplace-root>
```

手动测试 JSON 示例见 `references/architecture.md`。

## 发布提交

在 terr-marketplace 仓库根目录提交：

```bash
git add plugins/cc-statusline/ .claude-plugin/marketplace.json
git commit -m "sync: cc-statusline v<version> — <变更说明>"
git pull --rebase
git push
```

不要跳过 hooks；失败时修复原因后重新提交。

## 副本同步原则

cc-statusline 可能同时存在开发副本、marketplace 副本和运行时 cache 副本。文档不要写死某个机器上的绝对路径。

同步规则：
- 修改任一 `CLAUDE.local.md` 或 `references/*.md` 后，把同名文件同步到其它 cc-statusline 源码副本。
- marketplace 副本通常是发布入口；运行时 cache 副本只用于 Claude Code 实际执行。
- 修改源码后，除 build 外还要确保运行时 cache 使用的新 `dist/`，否则 settings.json 仍可能指向旧代码。
- 更新 cache 版本时必须同步 Claude Code 的 `plugins/installed_plugins.json`，否则 slash command 注册仍会指向旧 installPath。
- 若不确定有哪些副本，搜索 `plugins/**/cc-statusline` 或检查 Claude Code 插件 marketplace/cache 目录，不把搜索结果写回文档。
