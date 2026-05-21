# 发布流程 (Maintainer)

> 这是 **维护者** 发布新版本的流程。**终端用户** 使用 `/cc-statusline:update` 一键更新，无需执行以下步骤。

源码位于 terr-marketplace 仓库子目录 `plugins/cc-statusline/`。

## 发布步骤

1. 更新 `plugins/cc-statusline/package.json` 和 `plugins/cc-statusline/package-lock.json` 中的 `version`
2. 更新 `plugins/cc-statusline/.claude-plugin/plugin.json` 中的 `version`
3. 同步更新根 `.claude-plugin/marketplace.json` 中 cc-statusline 条目的 `version`
4. 提交并推送：

```bash
cd ~/.claude/plugins/marketplaces/terr-marketplace
git add plugins/cc-statusline/ .claude-plugin/marketplace.json
git commit -m "sync: cc-statusline v<version> — <变更说明>"
git pull --rebase && git push
```

5. 用户端执行 `/plugin install cc-statusline` 即可更新

## 修改后验证

1. `npm run build` 编译无错
2. 手动测试: `echo '{...}' | node dist/index.js` 检查 ANSI 输出
3. `claude plugin validate ~/.claude/plugins/marketplaces/terr-marketplace` 检查结构

## 参考文件同步

修改 `references/*.md` 时，需同步到两个位置:
```bash
# terr-marketplace → 工作目录
cp -r ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/references "C:/AI/m_projects/cc-statusline/"

# 工作目录 → terr-marketplace
cp -r "C:/AI/m_projects/cc-statusline/references/"* ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/references/
```
