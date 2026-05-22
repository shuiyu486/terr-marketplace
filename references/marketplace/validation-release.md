# Validation and release

用于 Windows / PowerShell JSON 维护、`claude plugin validate .` 排查，以及提交发布前检查。

## PowerShell 与 JSON 陷阱

Windows / PowerShell 下维护 JSON 时注意：

- 避免用 `ConvertTo-Json` 生成 `plugin.json` 或 `marketplace.json`。
- 避免裸 `Set-Content` / `Get-Content` 造成编码问题。
- 避免 `Set-Content -Encoding UTF8` 在旧 PowerShell 中写出 BOM。

推荐无 BOM UTF-8 写入方式：

```powershell
[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))
```

JSON 建议：

- 小文件优先手写或用编辑工具精确修改。
- 修改后用 JSON parser 验证。
- 不要依赖 PowerShell 默认编码。

## validate 失败排查

验证命令：

```bash
claude plugin validate .
```

常见问题：

| 现象 | 可能原因 | 处理 |
|---|---|---|
| JSON parse error | 逗号、引号、尾逗号错误 | 检查对应 JSON |
| source invalid | 未使用 `git-subdir` | 改为 git-subdir 结构 |
| path not found | `source.path` 指错 | 确认 `plugins/<name>` 存在 |
| version mismatch | 多个 version 未同步 | 按版本同步规则检查 |
| metadata missing | plugin.json 字段不完整 | 补齐 name/version/description 等 |

单独测试 JSON 可使用：

```powershell
Get-Content <file> -Raw | ConvertFrom-Json
```

如果怀疑编码问题，重写为无 BOM UTF-8。

## 发布前检查清单

提交或发布前检查：

```bash
claude plugin validate .
git status
```

检查项：

- `.claude-plugin/marketplace.json` 已更新。
- 插件目录下 `.claude-plugin/plugin.json` 已更新。
- 如存在 `package.json` / `package-lock.json`，version 已同步。
- 用户可见变更已 bump version。
- 没有把本机路径、临时文件、私有配置写进远程文件。
- 没有把插件级历史 bug 塞进根入口文件。
- PowerShell 写出的 JSON 没有 BOM / 转义异常。

提交信息建议：

```text
Add <plugin-name> plugin v<x.y.z>
Update <plugin-name> to v<x.y.z>
Fix <plugin-name> <short issue>
```
