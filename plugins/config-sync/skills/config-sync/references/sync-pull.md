# 方向 2：项目 → 本地（ccNovaTerm → local）

用户说"同步到本地"时触发。将 ccNovaTerm 模板应用到本地环境。**本地 clone 或远程获取均可。**

1. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
2. **读取项目模板** — 从 `$configDir`（本地项目或远程缓存）读取模板文件。**跳过文件级排除的文件**
3. **检测系统值** — 自动查找当前系统对应的实际路径：
   - nu.exe 完整路径（按优先级查找）
   - Git usr/bin 路径
   - 当前用户名
4. **备份本地配置** — 将现有配置文件备份到 `~\ccNovaTerm-backup\yyyyMMdd_HHmmss\`
5. **替换占位符** — 将模板中的占位符替换为实际值。**内置保护规则**：env.nu 代理行自动保留本地版本。**用户排除规则**：对于字段级排除，替换占位符后从备份中恢复被排除的行
6. **settings.json 合并** — 只添加/更新 `statusLine` 字段，保留用户已有的 API key、模型设置、权限等。

**合并实现**（UTF-8 安全，避免 BOM）：

```powershell
# 读取本地和模板的 settings.json
$localJson = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($localPath)) | ConvertFrom-Json
$tplContent = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($tplPath)) -replace '__USERNAME__', (Split-Path -Leaf $env:USERPROFILE)
$tplJson = $tplContent | ConvertFrom-Json

# 只更新 statusLine，保留其他所有字段
$localJson | Add-Member -NotePropertyName statusLine -NotePropertyValue $tplJson.statusLine -Force
$merged = $localJson | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($localPath, $merged, (New-Object System.Text.UTF8Encoding $false))
```

**注意**：`ConvertTo-Json` 在 PS5.1 中默认深度为 2，需显式指定 `-Depth` 以确保嵌套结构不被截断。写入必须用 `WriteAllText` 而非 `Set-Content`（防 BOM）。
7. **写入本地** — 写入本地配置路径，自动创建所需目录。**必须使用 UTF-8 编码**（`New-Object System.Text.UTF8Encoding $false`），`starship.toml` 尤其敏感。**跳过文件级排除的文件**（不覆盖）。文件路径见 `paths.md`——CLAUDE.local.md 写入 `$repoRoot\CLAUDE.local.md`（如 `$repoRoot` 不存在则跳过）。
8. **运行验证** — 执行语法、Unicode 完整性和文件大小检查
9. **报告结果** — 列出写入的文件、跳过的文件（含排除原因）、备份位置、下一步操作（重启 WezTerm 等）。如果模板来自远程缓存，注明来源

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
