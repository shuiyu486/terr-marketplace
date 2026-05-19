# 方向 2：项目 → 本地（ccNovaTerm → local）

用户说"同步到本地"时触发。将远程 ccNovaTerm 模板应用到本地环境。**模板始终从远程获取。**

1. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
2. **读取项目模板** — 从 `$configDir`（远程缓存，由第零步设置）读取模板文件。**跳过文件级排除的文件**
3. **检测系统值** — 自动查找当前系统对应的实际路径：
   - nu.exe 完整路径（按优先级查找）
   - Git usr/bin 路径
   - 当前用户名
4. **备份本地配置** — 将现有配置文件备份到 `~\ccNovaTerm-backup\yyyyMMdd_HHmmss\`
5. **替换占位符** — 将模板中的占位符替换为实际值。**内置保护规则**：env.nu 代理行自动保留本地版本。**用户排除规则**：对于字段级排除，替换占位符后从备份中恢复被排除的行
6. **写入本地** — 写入本地配置路径，自动创建所需目录。**必须使用 UTF-8 编码**（`New-Object System.Text.UTF8Encoding $false`），`starship.toml` 尤其敏感。**跳过文件级排除的文件**（不覆盖）。文件路径见 `paths.md`——CLAUDE.local.md 写入 `Join-Path $PWD.Path "CLAUDE.local.md"`（路径不可写则跳过）。
7. **运行验证** — 执行语法、Unicode 完整性和文件大小检查
8. **报告结果** — 列出写入的文件、跳过的文件（含排除原因）、备份位置、下一步操作（重启 WezTerm 等）

## 字段级排除的行级合并

当某文件有字段级排除规则时，在写入模板内容前：

```powershell
# 对于有字段级排除的文件，逐行处理
if ($excludeRules.ContainsKey($fname) -and $excludeRules[$fname][0] -ne "*") {
    $tplLines = $templatedContent -split "`n"
    $localLines = $localContent -split "`n"
    $mergedLines = @()
    for ($i = 0; $i -lt $tplLines.Count; $i++) {
        $excluded = $false
        foreach ($pattern in $excludeRules[$fname]) {
            if ($tplLines[$i].Contains($pattern)) { $excluded = $true; break }
        }
        if ($excluded -and $i -lt $localLines.Count) {
            $mergedLines += $localLines[$i]  # 保留本地行
        } else {
            $mergedLines += $tplLines[$i]     # 使用模板行
        }
    }
    $templatedContent = $mergedLines -join "`n"
}
```
