# skill-creator fork 同步账本

## 上游来源
- 仓库：https://github.com/anthropics/claude-plugins-official
- 路径：plugins/skill-creator
- 分支：main
- 最近同步基线：1d5ba6426aa27bab9dcf69e89b2f119609ce0885

## 本地插件
- 仓库：https://github.com/shuiyu486/terr-marketplace
- 路径：plugins/skill-creator
- 推送 remote：origin
- 推送分支：main

## 需要保留的本地魔改
- `.claude-plugin/plugin.json` — 保留 terr-marketplace 发布所需的 `version`、`repository`、`license`、`keywords` 等插件元数据；不要用上游精简版直接覆盖。
- `README.md` — 保留中文 marketplace 说明和安装后使用示例；上游 README 仅作为官方简介参考。
- `skills/skill-creator/SKILL.md` — 保留 frontmatter description 中增强的 `fix`、`repair`、`optimize`、`package` 等触发词；正文默认跟随上游。

## 跟随上游的内容
- 未在“需要保留的本地魔改”中列出的文件默认跟随上游。
- 已经回归上游或与上游一致的文件不要写入本地魔改清单；回归原因写进 commit message。

## 同步策略
- 对比策略：hash-first
- 自动应用：仅低风险变更
- 推送策略：用户确认同步后自动提交并推送；如果工作区不干净、remote/branch 不明确或存在冲突，则停止在提交前。
